# Failed Experiments Log

Mục tiêu: Ghi chép lại các thí nghiệm thất bại, các artifact không giải thích được, và các giả thuyết đã bị bác bỏ. 
Nguyên tắc: Không bao giờ xóa code/experiment cũ — chỉ cần ghi log tại sao nó thất bại.

---

## Template Ghi Chép
### [YYYY-MM-DD] Tên thí nghiệm/Giả thuyết
* **Mục tiêu:** (Ví dụ: Thử tăng chi từ 4 lên 16 để xem tail divergence có biến mất không)
* **Kết quả:** (Ví dụ: M2.5 Filter báo FAIL, Heatmap hiện vân sọc ngang)
* **Phân tích (Root Cause):** (Ví dụ: Do SVD truncation không ổn định ở vùng sai số thấp, hoặc do index ordering bị sai ở BM2)
* **Bài học:** (Ví dụ: Không nên tăng chi quá nhanh nếu chưa kiểm soát epsilon)

---

## Log

### [2026-06-16] Thử nghiệm baseline đầu tiên
* **Mục tiêu:** Chạy pipeline v0.1-alpha lần đầu.
* **Kết quả:** Pipeline chạy, nhưng Heatmap xuất hiện nhiễu ở cột χ=1.
* **Phân tích:** Lỗi do chưa chuẩn hóa ma trận (Trace = 1) trước khi nén.
* **Bài học:** Luôn kiểm tra tính CPTP (Trace Preserving) của ma trận trước mọi bước nén.