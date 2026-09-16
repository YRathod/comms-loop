"""Guard rails for scripts/muse_reply_daemon.py: it must stay a wrapper over the
responder's ack-marker path and never regrow its own reply drafting.

Run:  python -m unittest discover -s tests -v
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

import muse_reply_daemon as m  # noqa: E402
import comms_responder_daemon as d  # noqa: E402


def _mail(from_, to, thread, seq, type_, refs, body="hello"):
    refs_s = "[" + ", ".join(refs) + "]"
    return (
        f"---\nfrom: {from_}\nto: [{to}]\nthread: {thread}\nseq: {seq}\n"
        f"re-seq: none\ntype: {type_}\nrefs: {refs_s}\n---\n\n# {thread} s{seq}\n\n{body}\n"
    )


class MuseDaemonIsAWrapper(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.comms = self.root / "comms"
        for inbox in ("inbox_muse", "inbox_kimi", "inbox_fable"):
            (self.comms / inbox).mkdir(parents=True)
        (self.comms / "archive").mkdir()
        (self.comms / "LEDGER.md").write_text("| id | from | type | re | title | status |\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _drop(self, name, text):
        (self.comms / "inbox_muse" / name).write_text(text, encoding="utf-8")

    def test_action_mail_yields_marker_only_no_inbox_drop_no_seq(self):
        self._drop("20260101-000000-kimi-t1-s4-do-x.md", _mail("kimi", "muse", "t1", 4, "action", []))
        n = m.tick(self.comms)
        self.assertEqual(n, 1)
        markers = list((self.comms / "acks").glob("*.md"))
        self.assertEqual(len(markers), 1)
        text = markers[0].read_text(encoding="utf-8")
        self.assertIn("from: muse", text)
        self.assertIn("type: ack", text)
        self.assertIn("automated: true", text)
        self.assertNotRegex(text, r"(?m)^seq:")
        self.assertNotIn("Body preview", text)
        for inbox in ("inbox_kimi", "inbox_fable"):
            self.assertEqual(list((self.comms / inbox).iterdir()), [], f"daemon dropped mail into {inbox}")
        self.assertEqual(list((self.comms / "archive").iterdir()), [])

    def test_review_result_question_get_no_marker(self):
        for i, t in enumerate(("review", "result", "question")):
            self._drop(f"20260101-00000{i}-kimi-t2-s{i}-{t}.md", _mail("kimi", "muse", "t2", i, t, []))
        self.assertEqual(m.tick(self.comms), 0)
        self.assertFalse((self.comms / "acks").exists())

    def test_uses_responder_state_and_is_idempotent(self):
        self._drop("20260101-000000-fable-t3-s1-do-x.md", _mail("fable", "muse", "t3", 1, "action", []))
        self.assertEqual(m.tick(self.comms), 1)
        self.assertEqual(m.tick(self.comms), 0)
        self.assertTrue((self.comms / ".responder_state_muse.json").exists())


class NoReplyDraftingInSource(unittest.TestCase):
    def test_no_drafting_or_seq_functions(self):
        names = [n for n, f in inspect.getmembers(m, inspect.isfunction) if f.__module__ == m.__name__]
        bad = [n for n in names if re.search(r"draft|reply|next_seq|generate|response", n, re.IGNORECASE)]
        self.assertEqual(bad, [], f"reply-drafting functions present: {bad}")

    def test_source_never_writes_to_an_inbox(self):
        src = inspect.getsource(m).replace(m.__doc__ or "", "")
        self.assertNotIn("inbox_", src)
        self.assertNotIn("type: review", src)
        self.assertNotIn("seq:", src)

    def test_tick_delegates_to_responder(self):
        self.assertIs(m.responder, d)
        self.assertIn("process_inbox", inspect.getsource(m.tick))


if __name__ == "__main__":
    unittest.main()
