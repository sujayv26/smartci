import argparse
from pathlib import Path
from src.log_summarizer.parser import extract_diagnostics
from src.log_summarizer.llm import summarize_with_llm
def main():
 p=argparse.ArgumentParser();p.add_argument("log_file",type=Path);p.add_argument("--output",type=Path);a=p.parse_args()
 if not a.log_file.is_file():p.error(f"Log file does not exist: {a.log_file}")
 raw=a.log_file.read_text(encoding="utf-8",errors="replace");d=extract_diagnostics(raw);summary=summarize_with_llm(raw)
 report=f"# Build Log Summary\n\n- Total lines: {d['total_lines']}\n- Errors: {d['error_count']}\n- Warnings: {d['warning_count']}\n\n{summary}\n"
 if a.output:a.output.write_text(report,encoding="utf-8");print(f"Summary written to {a.output}")
 else:print(report)
if __name__=="__main__":main()
