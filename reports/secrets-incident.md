# Secret giả trong lịch sử Git — điền trong checkpoint 4

- Scanner và phiên bản: Gitleaks v8.30.1
- Commit chứa token giả: `1bdd849922156c868a5ee9293d68f5b72e242d2c`
- File, rule và kết quả quét lịch sử: lab-fake-secret.txt, rule lab24-synthetic-token; phát hiện 1 finding trong 11 commit; mã thoát 1 như dự đoán, token đã được che bởi --redact
- Kết quả quét file hiện tại: lần quét đầu tiên sạch, không có finding, mã thoát 0, không cần allowlist
- Nếu đây là credential thật, cần xử lý thế nào: thu hồi hoặc rotate tại dịch vụ cấp token, kiểm tra có ai dùng sai không, rồi xử lý các bản sao
- Vì sao xoá file khỏi HEAD hoặc pin dependency vẫn chưa đủ: lịch sử Git vẫn giữ commit cũ, pin dependency kiểm soát phiên bản package chứ không vô hiệu hóa credential đã bị lộ
