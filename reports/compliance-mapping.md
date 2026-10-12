# Compliance mapping — điền trong checkpoint 5

| Nguồn / yêu cầu | Control đã làm | Evidence file:dòng | Giới hạn |
|---|---|---|---|
| [Luật 91/2025/QH15](https://vanban.chinhphu.vn/?classid=1&docid=214590&pageid=27160&typegroup=) | Hồ sơ khách được gắn restricted; policy chặn khi dữ liệu này đi qua egress | agent/policy.py:60-63; agent/runner.py:39-67,115-126; reports/ledger.jsonl:24 | Chỉ là kiểm soát trong lab. Chưa đối chiếu điều khoản hay đánh giá căn cứ xử lý, quyền chủ thể và thời hạn lưu giữ; không kết luận tuân thủ |
| [NĐ 356/2025/NĐ-CP](https://vanban.chinhphu.vn/?docid=216387&pageid=27160&typegroupid=4) | Mỗi lần gọi tool có quyết định, lý do, principal, run và thời hạn; ledger có kiểm tra hash chain | agent/runner.py:155-172; agent/ledger.py:57-82,85-115; reports/ledger.jsonl:24 | Chưa đối chiếu điều khoản cụ thể. Hash chain trong một file không phát hiện xóa dòng cuối hoặc viết lại toàn bộ file |
| [Luật AI 134/2025/QH15](https://vanban.chinhphu.vn/?classid=1&docid=216334&orggroupid=1&pageid=27160) | Ticket được xem là nội dung không tin cậy; quyền đọc hồ sơ và quyền gửi ra ngoài được kiểm riêng tại ranh giới tool | agent/runner.py:39-67,83-126; tests/test_injection.py:69-142 | Chưa đối chiếu điều khoản cụ thể hoặc đánh giá yêu cầu quản trị/rủi ro theo luật; mock không đại diện hệ thống triển khai thật |
| [OWASP ASI01, ASI03, ASI04](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) | ASI01: replay lure; ASI03: kiểm principal/scope/purpose/TTL; ASI04: pin dependency và quét secret bằng hook | tests/test_injection.py:69-142; agent/policy.py:60-100; .pre-commit-config.yaml:1-6; requirements.lock:1-9; reports/secrets-incident.md:3-8 | Đây là đối chiếu chủ đề, không phải chứng nhận OWASP; kiểm soát supply chain mới ở mức lock và quét secret |

Trang Chính phủ xác nhận tên và số hiệu các văn bản.
