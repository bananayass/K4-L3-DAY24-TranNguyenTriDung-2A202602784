# Verification — điền trước khi nộp

- OS / Python / Gitleaks version:
- CP3a — `.venv/bin/python -m pytest tests/test_pii.py -v -s`: 2 passed; gold=118, pred=118, tp=118; precision=1.000; recall=1.000
- CP3b — `.venv/bin/python -m pytest tests/test_policy.py -v`: 4 passed
- CP3c — `.venv/bin/python -m pytest tests/test_obo.py tests/test_policy.py -v`: 9 passed; support_l1 bị chặn trước khi đọc hồ sơ, dpo đọc được theo quyền mô phỏng; ledger có metadata OBO
- `python -m pytest tests/ -q`:
- `pre-commit run --all-files`:
- Ledger verify:
- Các lỗi còn lại:
