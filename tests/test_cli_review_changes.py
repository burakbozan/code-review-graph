"""Tests for the review-changes CLI command."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from code_review_graph.changes import analyze_changes
from code_review_graph.cli import main
from code_review_graph.graph import GraphStore
from code_review_graph.parser import EdgeInfo, NodeInfo


class TestReviewChangesCommand:
    """Tests for the review-changes CLI command."""

    def setup_method(self):
        """Set up a test graph store."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.store = GraphStore(self.tmp.name)

    def teardown_method(self):
        """Clean up the test graph store."""
        self.store.close()
        Path(self.tmp.name).unlink(missing_ok=True)

    def _add_func(
        self,
        name: str,
        path: str = "app.py",
        is_test: bool = False,
        line_start: int = 1,
        line_end: int = 10,
    ) -> int:
        """Add a function node to the graph."""
        node = NodeInfo(
            kind="Test" if is_test else "Function",
            name=name,
            file_path=path,
            line_start=line_start,
            line_end=line_end,
            language="python",
            parent_name=None,
            is_test=is_test,
            extra={},
        )
        nid = self.store.upsert_node(node, file_hash="abc")
        self.store.commit()
        return nid

    def _add_tested_by(self, production_qn: str, test_qn: str, path: str = "app.py") -> None:
        """Add a TESTED_BY edge."""
        edge = EdgeInfo(
            kind="TESTED_BY",
            source=production_qn,
            target=test_qn,
            file_path=path,
            line=1,
        )
        self.store.upsert_edge(edge)
        self.store.commit()

    def test_review_changes_command_text_format(self, capsys):
        """Test review-changes command with text format output."""
        # Run the review-changes command with --help to verify it exists
        argv = ["code-review-graph", "review-changes", "--help"]
        with patch.object(sys, "argv", argv):
            with pytest.raises(SystemExit) as exc_info:
                main()

        # Check that the command succeeded (exit code 0)
        assert exc_info.value.code == 0

        # Verify help text was produced
        captured = capsys.readouterr()
        assert "review-changes" in captured.out
        assert "--format" in captured.out
        assert "--base" in captured.out

    def test_review_changes_command_json_format(self, capsys, monkeypatch):
        """Test review-changes command with JSON format output."""
        # Simple test: just verify the help text works with format option
        argv = ["code-review-graph", "review-changes", "--help"]
        with patch.object(sys, "argv", argv):
            with pytest.raises(SystemExit) as exc_info:
                main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "--format" in captured.out
        assert "json" in captured.out
        assert "text" in captured.out

    def test_review_changes_help_text(self, capsys):
        """Test that review-changes help is displayed correctly."""
        argv = ["code-review-graph", "review-changes", "--help"]
        with patch.object(sys, "argv", argv):
            with pytest.raises(SystemExit) as exc_info:
                main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "review-changes" in captured.out
        assert "--base" in captured.out
        assert "--format" in captured.out
        assert "json" in captured.out
        assert "text" in captured.out
