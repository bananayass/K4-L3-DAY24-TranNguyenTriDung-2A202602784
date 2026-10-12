# Verification — điền trước khi nộp

- OS / Python / Gitleaks version: Linux x86_64 / Python 3.12.3 / Gitleaks 8.30.1
- CP3a — `.venv/bin/python -m pytest tests/test_pii.py -v -s`: 2 passed; gold=118, pred=118, tp=118; precision=1.000; recall=1.000
- CP3b — `.venv/bin/python -m pytest tests/test_policy.py -v`: 4 passed
- CP3c — `.venv/bin/python -m pytest tests/test_obo.py tests/test_policy.py -v`: 9 passed; support_l1 bị chặn trước khi đọc hồ sơ, dpo đọc được theo quyền mô phỏng; ledger có metadata OBO
- CP3d — `.venv/bin/python -m pytest tests/test_split.py tests/test_obo.py tests/test_policy.py -v`: 10 passed; khách chỉ được nêu trong nội dung lure không bị đọc, khách có ticket liên quan vẫn được đọc nội dung đó
- CP3e — `.venv/bin/python -m pytest tests/test_ledger.py tests/test_split.py tests/test_obo.py tests/test_policy.py -v`: 13 passed; hash-chain nối đúng và phát hiện được dòng nào đã bị sửa
- CP4 — `.venv/bin/python -m pytest tests/test_supply_chain.py -v --basetemp=.pytest_tmp`: 3 passed
- Gitleaks lịch sử — 1 finding trong 11 commit, mã thoát 1 như dự đoán
- Gitleaks file hiện tại — không có finding, mã thoát 0, không cần allowlist
- python -m pip install --require-hashes -r requirements.lock: thành công, các package trong lock đã có sẵn
- pre-commit install: hook đã được cài tại .git/hooks/pre-commit
- `python -m pytest tests/ -q`:
- `pre-commit run --all-files`: Passed
- Ledger verify: test sửa dòng các cũ trong tests/test_ledger.py làm verify trả về False
- Các lỗi còn lại:
