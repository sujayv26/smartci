from unittest.mock import Mock,patch
import pytest
from src.log_summarizer.parser import extract_diagnostics
from src.log_summarizer.llm import summarize_with_llm
def test_parser_counts_errors_warnings():
 d=extract_diagnostics("INFO start\nERROR compiler failed\nWARNING deprecated API");assert d["error_count"]==1 and d["warning_count"]==1 and d["total_lines"]==3
def test_parser_rejects_empty():
 with pytest.raises(ValueError):extract_diagnostics("  ")
def test_llm_requires_key(monkeypatch):
 monkeypatch.delenv("GROQ_API_KEY",raising=False)
 with pytest.raises(RuntimeError,match="GROQ_API_KEY"):summarize_with_llm("ERROR failed")
def test_llm_mock_response():
 response=Mock(status_code=200);response.json.return_value={"choices":[{"message":{"content":"## Build Status\nFailed"}}]}
 with patch("src.log_summarizer.llm.requests.post",return_value=response):assert "Build Status" in summarize_with_llm("ERROR failed",api_key="test")
