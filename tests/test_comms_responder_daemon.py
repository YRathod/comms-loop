"""Guard rails for scripts/comms_responder_daemon.py.

The daemon may only write ack markers. These tests fail if it ever again
authors thread mail, assigns a seq, appends a ledger row, archives another
party's mail, or emits a body with a claim in it.

Run:  python -m unittest tests.test_comms_responder_daemon
"""
from __future__ import annotations

import inspect
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import comms_responder_daemon as d  # noqa: E402

# Words that only belong in a body written by an agent session.
CLAIM_WORDS = re.compile(
    r"\b(landed|fixed|verified|accepted|verdict|adopt|reject|recommend|approve|proceed|falsified|pass(?:ed)?)\b",
    re.IGNORECASE,
)


def _mail(from_, to, thread, seq, type_, refs, body="hello"):
    refs_s = "[" + ", ".join(refs) + "]"
    return (
        f"---\nfrom: {from_}\nto: [{to}]\nthread: {thread}\nseq: {seq}\n"
        f"re-seq: none\ntype: {type_}\nrefs: {refs_s}\n---\n\n# {thread} s{seq}\n\n{body}\n"
    )


class ResponderIsOnlyAnAcker(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.comms = self.root / "comms"
        (self.comms / "inbox_kimi").mkdir(parents=True)
        (self.comms / "archive").mkdir()
        (self.comms / "LEDGER.md").write_text("| id | from | type | re | title | status |\n", encoding="utf-8")
        self.ref = self.root / "docs" / "plan.md"
        self.ref.parent.mkdir()
        self.ref.write_text("plan", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _drop(self, name, text):
        p = self.comms / "inbox_kimi" / name
        p.write_text(text, encoding="utf-8")
        return p

    def test_action_mail_gets_one_marker_with_no_seq_and_no_claim(self):
        self._drop("20260101-000000-fable-t1-s1-do-x.md", _mail("fable", "kimi", "t1", 1, "action", ["docs/plan.md"]))
        n = d.process_inbox("kimi", self.comms, root=self.root)
        self.assertEqual(n, 1)
        markers = list((self.comms / "acks").glob("*.md"))
        self.assertEqual(len(markers), 1)
        text = markers[0].read_text(encoding="utf-8")
        self.assertIn("type: ack", text)
        self.assertIn("automated: true", text)
        self.assertIn(f"authored-by: {d.DAEMON_NAME}", text)
        self.assertIn("re: 20260101-000000-fable-t1-s1-do-x", text)
        self.assertIn("refs-check: PASS", text)
        self.assertNotRegex(text, r"(?m)^seq:")
        body = text.split("---", 2)[2]
        self.assertIsNone(CLAIM_WORDS.search(body), f"claim word in ack body:\n{body}")

    def test_non_action_mail_gets_no_marker(self):
        for t in ("result", "review", "protocol", "question", "blocker"):
            self._drop(f"20260101-00000{len(t)}-fable-t2-s1-{t}.md", _mail("fable", "kimi", "t2", 1, t, ["docs/plan.md"]))
        n = d.process_inbox("kimi", self.comms, root=self.root)
        self.assertEqual(n, 0)
        self.assertFalse((self.comms / "acks").exists())

    def test_daemon_never_archives_or_writes_mail_or_ledger(self):
        p = self._drop("20260101-000000-fable-t3-s1-do-x.md", _mail("fable", "kimi", "t3", 1, "action", ["docs/plan.md"]))
        ledger_before = (self.comms / "LEDGER.md").read_text(encoding="utf-8")
        d.process_inbox("kimi", self.comms, root=self.root)
        self.assertTrue(p.exists(), "incoming mail must stay in the inbox for the session")
        self.assertEqual(list((self.comms / "archive").iterdir()), [])
        self.assertEqual((self.comms / "LEDGER.md").read_text(encoding="utf-8"), ledger_before)
        for inbox in self.comms.glob("inbox_*"):
            if inbox.name != "inbox_kimi":
                self.fail(f"daemon created {inbox}")

    def test_second_pass_is_idempotent(self):
        self._drop("20260101-000000-fable-t4-s1-do-x.md", _mail("fable", "kimi", "t4", 1, "action", ["docs/plan.md"]))
        self.assertEqual(d.process_inbox("kimi", self.comms, root=self.root), 1)
        self.assertEqual(d.process_inbox("kimi", self.comms, root=self.root), 0)
        self.assertEqual(len(list((self.comms / "acks").glob("*.md"))), 1)

    def test_missing_ref_yields_fail_verdict(self):
        self._drop("20260101-000000-fable-t5-s1-do-x.md", _mail("fable", "kimi", "t5", 1, "action", ["docs/plan.md", "docs/nope.md"]))
        d.process_inbox("kimi", self.comms, root=self.root)
        text = next((self.comms / "acks").glob("*.md")).read_text(encoding="utf-8")
        self.assertIn("refs-check: FAIL", text)
        self.assertIn("- docs/nope.md", text)

    def test_two_mails_with_same_thread_and_seq_get_two_markers(self):
        # duplicate seqs are the case the protocol asks daemons to flag, never to collapse
        self._drop("20260101-000000-fable-t7-s5-first.md", _mail("fable", "kimi", "t7", 5, "action", []))
        self._drop("20260101-000100-grok-t7-s5-second.md", _mail("grok", "kimi", "t7", 5, "action", []))
        self.assertEqual(d.process_inbox("kimi", self.comms, root=self.root), 2)
        markers = sorted((self.comms / "acks").glob("*.md"))
        self.assertEqual(len(markers), 2)
        texts = [p.read_text(encoding="utf-8") for p in markers]
        self.assertTrue(any("re: 20260101-000000-fable-t7-s5-first" in t for t in texts))
        self.assertTrue(any("re: 20260101-000100-grok-t7-s5-second" in t for t in texts))

    def test_self_addressed_mail_is_ignored(self):
        self._drop("20260101-000000-kimi-t6-s1-note.md", _mail("kimi", "kimi", "t6", 1, "action", []))
        self.assertEqual(d.process_inbox("kimi", self.comms, root=self.root), 0)


class NoContentGeneratorsInSource(unittest.TestCase):
    """Static guard: the module must not grow thread-specific reply templates again."""

    def test_no_generator_functions(self):
        names = [n for n, _ in inspect.getmembers(d, inspect.isfunction)]
        offenders = [n for n in names if "generate" in n.lower() or "response" in n.lower()]
        self.assertEqual(offenders, [], f"content-generating functions present: {offenders}")

    def test_ack_body_is_a_constant_without_claims(self):
        self.assertIsInstance(d.ACK_BODY, str)
        self.assertIsNone(CLAIM_WORDS.search(d.ACK_BODY))

    def test_source_has_no_thread_specific_branches(self):
        src = inspect.getsource(d).replace(d.__doc__ or "", "")  # the module docstring may name history
        for needle in ("sympy-symbolic", "compute-effectiveness", "metrology", "repairs landed", "type: result", "type: review"):
            self.assertNotIn(needle, src, f"source still mentions {needle!r}")


if __name__ == "__main__":
    unittest.main()
