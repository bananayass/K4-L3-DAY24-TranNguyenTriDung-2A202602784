# Verification — điền trước khi nộp

- OS / Python / Gitleaks version:
- CP3a — `.venv/bin/python -m pytest tests/test_pii.py -v -s`: 2 passed; gold=118, pred=118, tp=118; precision=1.000; recall=1.000.
- CP3b — `.venv/bin/python -m pytest tests/test_policy.py -v`: 4 passed.
- `python -m pytest tests/ -q`:
- `pre-commit run --all-files`:
- Ledger verify:
- Các lỗi còn lại:
