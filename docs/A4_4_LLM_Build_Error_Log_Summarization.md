# SMART CI — ASSIGNMENT 4

## A4_4: LLM-Based Build/Error-Log Summarization

**Name:** Sujay V | **USN:** 24BTRAO041  
**GitHub Repository:** https://github.com/sujayv26/smartci

### 1. Aim
To implement an LLM-based utility that accepts a CI build log, extracts important diagnostic information, and generates a concise explanation of build status, key errors, likely root cause, and recommended fixes.

### 2. Introduction
CI pipelines generate long logs containing informational messages, warnings, errors, and stack traces. Reading the complete log manually can take time. This assignment uses Python regular expressions to identify diagnostic lines and an external Large Language Model API to produce a human-readable summary. Log content is treated as untrusted input so instructions embedded in logs are not followed.

### 3. Tools and Technologies
- Python 3.12
- Groq Chat Completions API (OpenAI-compatible REST interface)
- Llama 3.3 70B Versatile model (default; configurable)
- Requests for HTTP communication
- Regular expressions for diagnostic extraction
- pytest and unittest.mock for automated testing
- Git and GitHub

### 4. Implementation
**4.1 Diagnostic extraction — `src/log_summarizer/parser.py`**  
The `extract_diagnostics()` function reads the log line by line. Regular expressions identify error, fatal, failed, failure, exception, and warning terms. It records original line numbers, captures stack-trace-like lines, counts total lines, and reports frequent error terms. Empty input is rejected.

**4.2 LLM summarization — `src/log_summarizer/llm.py`**  
The `summarize_with_llm()` function sends the log to Groq's chat-completions endpoint. Its system prompt requests a structured report with Build Status, Key Errors, Likely Root Cause, Recommended Fixes, and Evidence. It explicitly treats log contents as untrusted data. The API key is read from `GROQ_API_KEY`; HTTP errors, missing credentials, unexpected responses, and empty summaries are handled.

**4.3 Command-line interface — `scripts/summarize_build_log.py`**  
The CLI accepts a log-file path and optional Markdown output path. It extracts diagnostic counts, requests the LLM summary, and combines both into a Markdown report.

### 5. Execution and Configuration
Install dependencies:
```bash
python -m pip install -r requirements.txt
```
Set the API key in PowerShell:
```powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```
Optional model setting:
```powershell
$env:GROQ_MODEL="llama-3.3-70b-versatile"
```
Run:
```bash
python -m scripts.summarize_build_log data/sample_build.log --output docs/sample_summary.md
```
Never commit a real API key. The `.env.example` file contains placeholders only.

### 6. Experiments and Observations
**Experiment 1 — Diagnostic extraction:** A sample build log with a warning, error messages, and informational messages is passed to the parser. The parser separates diagnostic lines and preserves their source line numbers.

**Experiment 2 — LLM client validation:** Automated tests mock the HTTP response to verify request handling and summary extraction. Another test verifies that execution stops with a clear message when `GROQ_API_KEY` is missing. These tests do not require a real API key or network access.

**Experiment 3 — Error handling:** Empty log input and missing credentials are rejected. A live provider summary requires a personal Groq API key and must be run locally.

### 7. Screenshots and Results
Add actual screenshots from your local run:
- Figure 1. Terminal command and generated Markdown report.
- Figure 2. LLM summary with the five requested headings.
- Figure 3. Successful pytest output for summarizer tests.

**Verified test scope:** Parser and mocked API integration are tested automatically. A live provider response is not claimed by the unit tests.

### 8. Learning Outcomes
- Understood the structure of CI build logs.
- Extracted errors and warnings using regular expressions.
- Learned how an LLM converts raw logs into a structured explanation.
- Protected API credentials using environment variables.
- Practised HTTP request and error handling.
- Used mocks to test an external API integration without network calls.

### 9. Conclusion
An LLM-based build/error-log summarization utility was implemented using Python, regular expressions, and Groq's chat-completions API. It extracts diagnostic context and requests an explanation with likely causes and recommended fixes. Automated tests validate parsing, credential handling, and the mocked API response path. Live summarization can be performed after configuring a personal API key.

### 10. GitHub Repository
https://github.com/sujayv26/smartci
