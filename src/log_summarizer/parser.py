import re
from collections import Counter
def extract_diagnostics(log_text: str)->dict:
 if not log_text or not log_text.strip():raise ValueError("Log text must not be empty")
 errors,warnings,stack=[],[],[];lines=log_text.splitlines()
 for i,line in enumerate(lines,1):
  clean=line.strip()
  if re.search(r"\b(error|fatal|failed|failure|exception)\b",clean,re.I):errors.append(f"L{i}: {clean}")
  elif re.search(r"\b(warn|warning)\b",clean,re.I):warnings.append(f"L{i}: {clean}")
  if re.match(r'^(\s+at\s|\s*File "|\s*Traceback)',line):stack.append(f"L{i}: {clean}")
 terms=Counter(w.lower() for line in errors for w in re.findall(r"[A-Za-z]+",line))
 return {"total_lines":len(lines),"error_count":len(errors),"warning_count":len(warnings),"errors":errors[:80],"warnings":warnings[:80],"stack_trace":stack[:80],"frequent_error_terms":dict(terms.most_common(8))}
