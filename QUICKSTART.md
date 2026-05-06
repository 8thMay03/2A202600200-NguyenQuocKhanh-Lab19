# 🚀 QUICKSTART GUIDE

Hướng dẫn nhanh để chạy hệ thống GraphRAG trong 5 phút!

## Bước 1: Kiểm tra cài đặt ✅

Tất cả dependencies đã được cài đặt thành công! Chạy lệnh sau để kiểm tra:

```bash
python test_setup.py
```

## Bước 2: Cấu hình OpenAI API Key 🔑

1. Mở file `.env` trong thư mục gốc
2. Thay thế `your_openai_api_key_here` bằng API key thực của bạn:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**Lấy API key ở đâu?**
- Truy cập: https://platform.openai.com/api-keys
- Đăng nhập và tạo API key mới
- Copy và paste vào file `.env`

## Bước 3: Chạy hệ thống 🎯

### Option A: Chạy toàn bộ pipeline (Khuyến nghị)

```bash
python main.py
```

Script này sẽ:
1. ✅ Trích xuất triples từ corpus (khoảng 2-3 phút)
2. ✅ Xây dựng knowledge graph
3. ✅ Tạo visualization
4. ✅ Đánh giá 20 câu hỏi trên cả GraphRAG và Flat RAG
5. ✅ Lưu kết quả vào `output/`

### Option B: Chạy từng bước trong Jupyter Notebook

```bash
jupyter notebook notebook.ipynb
```

Notebook cho phép bạn:
- Chạy từng cell một
- Xem kết quả trung gian
- Thử nghiệm với các tham số khác nhau

## Bước 4: Xem kết quả 📊

Sau khi chạy xong, kiểm tra thư mục `output/`:

```
output/
├── triples.json                # Các bộ ba đã trích xuất
├── knowledge_graph.json        # Đồ thị tri thức
├── graph_visualization.png     # Hình ảnh đồ thị
└── evaluation_results.json     # Kết quả so sánh
```

### Xem visualization:

```bash
# Windows
start output/graph_visualization.png

# Linux/Mac
open output/graph_visualization.png
```

## Troubleshooting 🔧

### Lỗi: "OpenAI API key not found"
- Kiểm tra file `.env` đã được tạo
- Đảm bảo API key đúng format: `sk-proj-...`
- Kiểm tra API key còn credit tại: https://platform.openai.com/usage

### Lỗi: "Module not found"
```bash
pip install -r requirements.txt
```

### Lỗi: "Rate limit exceeded"
- API key của bạn đã hết quota
- Đợi một chút hoặc nâng cấp plan

### Lỗi: ChromaDB connection
```bash
# Xóa database cũ và thử lại
rm -rf chroma_db/
python main.py
```

## Chi phí ước tính 💰

Với corpus mẫu (20 đoạn văn):
- **Trích xuất triples**: ~$0.10 - $0.20
- **Truy vấn 20 câu hỏi**: ~$0.05 - $0.10
- **Tổng**: ~$0.15 - $0.30

## Tùy chỉnh 🎨

### Thay đổi số câu hỏi đánh giá

Mở `main.py` và sửa danh sách `questions` trong hàm `evaluate_systems()`.

### Thay đổi corpus

Thay thế nội dung trong `data/tech_company_corpus.txt` bằng dữ liệu của bạn.

### Thay đổi max_hops

Trong `main.py`, tìm dòng:
```python
graph_result = graph_rag.answer_query(question, max_hops=2, verbose=False)
```

Thay `max_hops=2` thành `max_hops=3` để duyệt xa hơn trong đồ thị.

## Câu hỏi thường gặp ❓

**Q: Tôi có thể dùng model khác thay vì GPT-4o-mini không?**
A: Có! Mở các file trong `src/` và thay đổi `model="gpt-4o-mini"` thành model bạn muốn (ví dụ: `gpt-4`, `gpt-3.5-turbo`).

**Q: Làm sao để dùng Neo4j thay vì NetworkX?**
A: Uncomment phần Neo4j trong `src/graph_builder.py` và cấu hình connection trong `.env`.

**Q: Kết quả có thể khác nhau mỗi lần chạy không?**
A: Có, vì LLM có tính ngẫu nhiên. Để kết quả ổn định hơn, giảm `temperature` trong các API calls.

**Q: Tôi có thể chạy offline không?**
A: Không hoàn toàn, vì cần OpenAI API. Nhưng bạn có thể dùng local LLM như Ollama với một số chỉnh sửa.

## Tiếp theo 🎓

1. Đọc kỹ `README.md` để hiểu chi tiết về kiến trúc
2. Thử nghiệm với corpus của riêng bạn
3. So sánh kết quả GraphRAG vs Flat RAG
4. Viết báo cáo phân tích

## Hỗ trợ 💬

Nếu gặp vấn đề:
1. Chạy `python test_setup.py` để kiểm tra
2. Đọc phần Troubleshooting trong `README.md`
3. Kiểm tra error message cẩn thận
4. Liên hệ giảng viên/trợ giảng

---

**Chúc bạn thành công! 🎉**
