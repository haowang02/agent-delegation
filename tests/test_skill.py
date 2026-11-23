"""Check skill packaging, reference links, shell syntax, and installed CLI help."""

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "agent-delegation"
SKILL_DIR = ROOT / "skills" / SKILL_NAME
SKILL_MD = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"

# binary -> reference file, and the flags that reference must document
IMPLEMENTERS = {
    "codex": ("codex.md", ["exec", "--json", "-o", "-s", "resume"]),
    "claude": ("claude.md", ["-p", "--permission-mode", "--output-format", "stream-json", "--resume"]),
    "opencode": ("opencode.md", ["run", "--format", "--agent", "--auto", "--model", "--session"]),
    "pi": ("pi.md", ["--mode", "--no-approve", "--tools", "--continue", "--session"]),
    "agy": ("agy.md", ["--new-project", "--add-dir", "--print", "--sandbox", "--conversation"]),
}

HELP_ARGS = {
    "codex": ["exec", "--help"],
    "opencode": ["run", "--help"],
}


def read_frontmatter(text):
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    end = text.index("\n---\n", 4)
    block = text[4:end]
    fields = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        nested = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*)$", line)
        top = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if top:
            key, value = top.group(1), top.group(2).strip()
            fields[key] = "" if value in (">-", "|", ">") else value
        elif nested and key is not None:
            fields[f"{key}.{nested.group(1)}"] = nested.group(2).strip()
        elif key is not None:
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, text[end + 5 :]


class FrontmatterTest(unittest.TestCase):
    def setUp(self):
        self.frontmatter, self.body = read_frontmatter(SKILL_MD.read_text(encoding="utf-8"))

    def test_name_matches_directory_and_rules(self):
        name = self.frontmatter["name"]
        self.assertEqual(name, SKILL_DIR.name)
        self.assertRegex(name, r"^[a-z0-9-]+$")
        self.assertLessEqual(len(name), 64)

    def test_description_names_supported_clis_and_fits_cap(self):
        description = self.frontmatter["description"]
        self.assertLess(len(description), 1024, "some orchestrators hard-cap the description")
        for phrase in ("Codex", "Claude Code", "OpenCode", "Pi", "Antigravity"):
            self.assertIn(phrase, description)

    def test_declares_license_and_version(self):
        self.assertEqual(self.frontmatter.get("license"), "MIT")
        self.assertRegex(self.frontmatter.get("metadata.version", ""), r"^\d+\.\d+\.\d+$")


class ProgressiveDisclosureTest(unittest.TestCase):
    def setUp(self):
        self.body = read_frontmatter(SKILL_MD.read_text(encoding="utf-8"))[1]

    def test_skill_md_stays_an_overview(self):
        self.assertLess(len(self.body.splitlines()), 500)

    def test_routing_says_when_to_load_each_reference(self):
        for binary, (name, _) in IMPLEMENTERS.items():
            with self.subTest(binary=binary):
                self.assertRegex(
                    self.body,
                    rf"\|\s*[^|\n]*\|\s*`{binary}`\s*\|\s*\[[^\]\n]+\]\(references/{re.escape(name)}\)",
                    "each CLI needs a routing row: binary -> the reference to read before dispatching",
                )

    def test_local_markdown_links_resolve(self):
        pages = [ROOT / "README.md", SKILL_MD, *sorted(REFS.glob("*.md"))]
        for page in pages:
            text = page.read_text(encoding="utf-8")
            for target in re.findall(r"\]\((?!https?:|#)([^)#]+)(?:#[^)]*)?\)", text):
                with self.subTest(page=page.name, target=target):
                    self.assertTrue((page.parent / target).is_file())

    def test_long_references_have_a_table_of_contents(self):
        for path in sorted(REFS.glob("*.md")):
            with self.subTest(reference=path.name):
                text = path.read_text(encoding="utf-8")
                if len(text.splitlines()) > 100:
                    self.assertIn("Contents", text, f"{path.name} needs a table of contents")

    def test_no_orphan_references(self):
        body = SKILL_MD.read_text(encoding="utf-8")
        for path in sorted(REFS.glob("*.md")):
            with self.subTest(reference=path.name):
                self.assertIn(f"references/{path.name}", body)


class PerAgentReferenceTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which("bash"), "bash not installed")
    def test_dispatch_and_resume_examples_parse_as_shell(self):
        for binary, (name, _) in IMPLEMENTERS.items():
            with self.subTest(binary=binary):
                text = (REFS / name).read_text(encoding="utf-8")
                snippets = re.findall(r"```bash\n(.*?)\n```", text, flags=re.DOTALL)
                self.assertGreaterEqual(len(snippets), 2, "show dispatch and resume commands")
                for snippet in snippets:
                    completed = subprocess.run(
                        ["bash", "-n"], input=snippet, capture_output=True, text=True, timeout=10
                    )
                    self.assertEqual(completed.returncode, 0, completed.stderr)


class ManifestTest(unittest.TestCase):
    def setUp(self):
        self.plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.market = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )

    def test_plugin_manifest_points_at_the_skill(self):
        self.assertEqual(self.plugin["name"], SKILL_NAME)
        self.assertTrue((ROOT / "skills" / self.plugin["name"] / "SKILL.md").exists())
        self.assertIn(SKILL_NAME, self.plugin["homepage"])

    def test_marketplace_and_frontmatter_agree_on_version(self):
        frontmatter = read_frontmatter(SKILL_MD.read_text(encoding="utf-8"))[0]
        self.assertEqual(self.market["plugins"][0]["name"], SKILL_NAME)
        self.assertEqual(self.market["plugins"][0]["version"], self.plugin["version"])
        self.assertEqual(self.market["metadata"]["version"], self.plugin["version"])
        self.assertEqual(frontmatter.get("metadata.version"), self.plugin["version"])

    def test_readme_install_matches_repo_name(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"npx skills add haowang02/{SKILL_NAME}", readme)


class FlagParityTest(unittest.TestCase):
    """Compare documented flags with the installed CLI's own help output."""

    def test_documented_flags_exist(self):
        for binary, (name, flags) in IMPLEMENTERS.items():
            with self.subTest(binary=binary):
                reference = (REFS / name).read_text(encoding="utf-8")
                for flag in flags:
                    self.assertIn(flag, reference, f"{name} does not document {binary} {flag}")
                if shutil.which(binary) is None:
                    self.skipTest(f"{binary} not installed")
                # Some CLIs put usage text on stderr even when help succeeds.
                completed = subprocess.run(
                    [binary, *HELP_ARGS.get(binary, ["--help"])],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                help_text = completed.stdout + completed.stderr
                for flag in flags:
                    self.assertIn(flag, help_text, f"{binary} does not advertise {flag}")


if __name__ == "__main__":
    unittest.main()
