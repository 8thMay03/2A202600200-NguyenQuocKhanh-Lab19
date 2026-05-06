# 👋 BẮT ĐẦU TỪ ĐÂY!

Chào mừng bạn đến với Lab 19: Xây dựng Hệ thống GraphRAG! 🎉

## 🎯 Bạn đang ở đâu?

Đây là dự án hoàn chỉnh về GraphRAG (Graph-based Retrieval Augmented Generation) - một hệ thống AI tiên tiến để trả lời câu hỏi phức tạp bằng cách sử dụng đồ thị tri thức.

## 🚦 Lộ trình 3 bước

### Bước 1: Cài đặt (5 phút) ⚙️

```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Tạo file .env
cp .env.example .env

# 3. Thêm OpenAI API key vào .env
# Mở file .env và thay thế your_openai_api_key_here

# 4. Test cài đặt
python test_setup.py
```

**Lấy API key ở đâu?** → https://platform.openai.com/api-keys

### Bước 2: Chạy thử (10 phút) 🚀

```bash
# Chạy toàn bộ hệ thống
python main.py
```

Hoặc sử dụng Jupyter Notebook:
```bash
jupyter notebook notebook.ipynb
```

### Bước 3: Xem kết quả (5 phút) 📊

Kiểm tra thư mục `output/`:
- `graph_visualization.png` - Hình ảnh đồ thị tri thức
- `evaluation_results.json` - Kết quả so sánh
- `triples.json` - Các bộ ba đã trích xuất

## 📚 Tài liệu nào đọc trước?

### Nếu bạn muốn chạy nhanh:
👉 **[QUICKSTART.md](QUICKSTART.md)** - 5 phút để chạy hệ thống

### Nếu bạn muốn hiểu sâu:
👉 **[README.md](README.md)** - Tài liệu đầy đủ từ A-Z

### Nếu bạn muốn hiểu kiến trúc:
👉 **[ARCHITECTURE.md](ARCHITECTURE.md)** - Chi tiết kỹ thuật

### Nếu bạn cần nộp bài:
👉 **[SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)** - Hướng dẫn nộp bài

### Nếu bạn muốn xem tổng quan:
👉 **[INDEX.md](INDEX.md)** - Chỉ mục tất cả tài liệu

## 🎓 Bạn sẽ học được gì?

1. **Entity & Relation Extraction** - Trích xuất thông tin từ văn bản
2. **Knowledge Graph** - Xây dựng đồ thị tri thức
3. **Multi-hop Reasoning** - Suy luận qua nhiều bước
4. **RAG Systems** - So sánh GraphRAG vs Flat RAG
5. **System Evaluation** - Đánh giá hiệu suất hệ thống

## 🎯 Mục tiêu cuối cùng

Sau khi hoàn thành lab, bạn sẽ có:

✅ Hệ thống GraphRAG hoạt động hoàn chỉnh
✅ Đồ thị tri thức về các công ty công nghệ
✅ Kết quả so sánh GraphRAG vs Flat RAG
✅ Báo cáo phân tích chi tiết
✅ Hiểu biết sâu về Graph-based AI

## ⚡ Quick Commands

```bash
# Test cài đặt
python test_setup.py

# Chạy hệ thống
python main.py

# Chạy notebook
jupyter notebook notebook.ipynb

# Xem visualization
# Windows: start output/graph_visualization.png
# Mac: open output/graph_visualization.png
# Linux: xdg-open output/graph_visualization.png
```

## 🆘 Gặp vấn đề?

### Lỗi: "OpenAI API key not found"
→ Kiểm tra file `.env` đã có API key chưa

### Lỗi: "Module not found"
→ Chạy lại: `pip install -r requirements.txt`

### Lỗi khác?
→ Đọc phần Troubleshooting trong [README.md](README.md)

## 💰 Chi phí

- **Extraction**: ~$0.10-$0.20
- **20 câu hỏi**: ~$0.10-$0.20
- **Tổng**: ~$0.20-$0.40

## 📞 Cần hỗ trợ?

1. Đọc [QUICKSTART.md](QUICKSTART.md)
2. Chạy `python test_setup.py`
3. Đọc phần Troubleshooting
4. Hỏi trên forum/group
5. Liên hệ giảng viên

## 🎉 Sẵn sàng bắt đầu?

### Lộ trình khuyến nghị:

**Ngày 1** (1-2 giờ):
1. Đọc START_HERE.md (file này) ✅
2. Đọc QUICKSTART.md
3. Cài đặt và chạy test
4. Chạy main.py lần đầu

**Ngày 2** (2-3 giờ):
1. Đọc README.md
2. Đọc ARCHITECTURE.md
3. Chạy notebook.ipynb
4. Thử nghiệm với các câu hỏi khác

**Ngày 3** (2-3 giờ):
1. Phân tích kết quả
2. Viết báo cáo
3. Đọc SUBMISSION_GUIDE.md
4. Chuẩn bị nộp bài

## 🚀 Bắt đầu ngay!

```bash
# Bước 1: Cài đặt
pip install -r requirements.txt

# Bước 2: Cấu hình
cp .env.example .env
# Thêm API key vào .env

# Bước 3: Test
python test_setup.py

# Bước 4: Chạy
python main.py

# Bước 5: Xem kết quả
# Mở output/graph_visualization.png
```

## 📖 Đọc tiếp

Sau khi chạy thành công, đọc:
- [ARCHITECTURE.md](ARCHITECTURE.md) - Hiểu cách hệ thống hoạt động
- [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md) - Chuẩn bị nộp bài

---

**🎯 Mục tiêu của bạn**: Hiểu và xây dựng được hệ thống GraphRAG

**⏱️ Thời gian ước tính**: 6-8 giờ (bao gồm đọc, code, và viết báo cáo)

**💪 Độ khó**: Trung bình - Nâng cao

**🎓 Kiến thức cần có**: Python, cơ bản về AI/ML, đọc hiểu tiếng Anh

---

**Chúc bạn thành công! Bắt đầu từ [QUICKSTART.md](QUICKSTART.md) ngay! 🚀**
