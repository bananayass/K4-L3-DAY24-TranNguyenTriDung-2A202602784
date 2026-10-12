# Baseline — điền trong checkpoint 1

1. Agent có identity mỗi run chưa? Dẫn file/hàm: chưa vì naive loop không toạn hoặc ghi agentid hay runid cho từng lần chạy trong file (agent/loop.py, hàm _naive_loop)
2. Ai cho phép `http_post`? Dẫn file/hàm: Không có bước kiểm tra quyền trước khi gửi, khi tìm thấy dữ liệu khách hàng naive_loop() gọi http_pót luôn, giới hạn vào sink localhost để lab an toàn loop.py line 34 và tools.py line 68
3. Nếu gửi sai PII ra sink, bằng chứng ở đâu? Dẫn file/hàm: Bằng chứng là dòng ghi trong reports/sink.log file này sink lưu cả đường dẫn POST và nội dung gửi lên body, nên có thể kiểm tra record khách hàng nào đã bị gửi. Hàm do_POST() trong sink/sink.py ghi dòng này