# Verification — điền trước khi nộp

- OS / Python / Gitleaks version:
- CP3a — `.venv/bin/python -m pytest tests/test_pii.py -v -s`: 2 passed; gold=118, pred=118, tp=118; precision=1.000; recall=1.000
- CP3b — `.venv/bin/python -m pytest tests/test_policy.py -v`: 4 passed
- CP3c — `.venv/bin/python -m pytest tests/test_obo.py tests/test_policy.py -v`: 9 passed; support_l1 bị chặn trước khi đọc hồ sơ, dpo đọc được theo quyền mô phỏng; ledger có metadata OBO
- CP3d — `.venv/bin/python -m pytest tests/test_split.py tests/test_obo.py tests/test_policy.py -v`: 10 passed; khách chỉ được nêu trong nội dung lure không bị đọc, khách có ticket liên quan vẫn được đọc nội dung đó
- CP3e — `.venv/bin/python -m pytest tests/test_ledger.py tests/test_split.py tests/test_obo.py tests/test_policy.py -v`: 13 passed; hash-chain nối đúng và phát hiện được dòng nào đã bị sửa
- `python -m pytest tests/ -q`:
- `pre-commit run --all-files`:
- Ledger verify: test sửa dòng các cũ trong tests/test_ledger.py làm verify trả về False
- Các lỗi còn lại:
