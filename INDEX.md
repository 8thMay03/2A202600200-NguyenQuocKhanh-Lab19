# 📚 CHỈ MỤC TÀI LIỆU - LAB 19 GRAPHRAG

## 🎯 Bắt đầu nhanh

1. **[QUICKSTART.md](QUICKSTART.md)** - Hướng dẫn chạy hệ thống trong 5 phút
   - Cài đặt dependencies
   - Cấu hình API key
   - Chạy và xem kết quả

2. **[README.md](README.md)** - Tài liệu chính đầy đủ
   - Mục tiêu bài học
   - Hướng dẫn chi tiết từng bước
   - Troubleshooting

## 🏗️ Kiến trúc & Kỹ thuật

3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Kiến trúc hệ thống
   - Tổng quan kiến trúc
   - Chi tiết các module
   - Luồng dữ liệu
   - So sánh GraphRAG vs Flat RAG

## 📝 Nộp bài

4. **[SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)** - Hướng dẫn nộp bài
   - Checklist trước khi nộp
   - Nội dung cần nộp
   - Template báo cáo
   - Tiêu chí chấm điểm

## 📂 Cấu trúc dự án

```
Lab19_GraphRAG/
│
├── 📄 Tài liệu
│   ├── README.md              # Tài liệu chính
│   ├── QUICKSTART.md          # Hướng dẫn nhanh
│   ├── ARCHITECTURE.md        # Kiến trúc hệ thống
│   ├── SUBMISSION_GUIDE.md    # Hướng dẫn nộp bài
│   └── INDEX.md               # File này
│
├── 🐍 Mã nguồn chính
│   ├── main.py                # Script chính
│   ├── test_setup.py          # Test cài đặt
│   └── notebook.ipynb         # Jupyter notebook
│
├── 📦 Source code
│   └── src/
│       ├── entity_extraction.py    # Trích xuất thực thể
│       ├── graph_builder.py        # Xây dựng đồ thị
│       ├── graph_rag.py            # GraphRAG engine
│       └── flat_rag.py             # Flat RAG baseline
│
├── 📊 Dữ liệu
│   └── data/
│       └── tech_company_corpus.txt # Corpus mẫu
│
├── 📈 Kết quả (sau khi chạy)
│   └── output/
│       ├── triples.json            # Các bộ ba
│       ├── knowledge_graph.json    # Đồ thị
│       ├── graph_visualization.png # Hình ảnh
│       └── evaluation_results.json # Kết quả đánh giá
│
└── ⚙️ Cấu hình
    ├── requirements.txt       # Dependencies
    ├── .env.example          # Template API key
    ├── .env                  # API key (không commit)
    └── .gitignore            # Git ignore rules
```

## 🚀 Quy trình làm việc

### Lần đầu tiên

1. Đọc [QUICKSTART.md](QUICKSTART.md)
2. Cài đặt dependencies: `pip install -r requirements.txt`
3. Cấu hình `.env` với OpenAI API key
4. Test: `python test_setup.py`
5. Chạy: `python main.py`

### Hiểu sâu hơn

6. Đọc [ARCHITECTURE.md](ARCHITECTURE.md) để hiểu kiến trúc
7. Xem code trong `src/` để hiểu implementation
8. Chạy `notebook.ipynb` để thử nghiệm từng bước

### Nộp bài

9. Đọc [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)
10. Chuẩn bị báo cáo theo template
11. Kiểm tra checklist
12. Nộp bài

## 📖 Đọc theo thứ tự khuyến nghị

### Cho người mới bắt đầu

1. **README.md** (Phần 1-3) - Hiểu mục tiêu và cài đặt
2. **QUICKSTART.md** - Chạy thử hệ thống
3. **README.md** (Phần 4-6) - Hiểu chi tiết từng bước
4. **ARCHITECTURE.md** - Hiểu kiến trúc
5. **SUBMISSION_GUIDE.md** - Chuẩn bị nộp bài

### Cho người có kinh nghiệm

1. **QUICKSTART.md** - Chạy nhanh
2. **ARCHITECTURE.md** - Hiểu kiến trúc
3. Đọc code trong `src/`
4. **SUBMISSION_GUIDE.md** - Nộp bài

## 🔍 Tìm kiếm nhanh

### Tôi muốn...

- **Cài đặt hệ thống** → [QUICKSTART.md](QUICKSTART.md) - Bước 1
- **Hiểu GraphRAG hoạt động như thế nào** → [ARCHITECTURE.md](ARCHITECTURE.md) - Phần 3
- **So sánh GraphRAG vs Flat RAG** → [ARCHITECTURE.md](ARCHITECTURE.md) - Phần "So sánh"
- **Sửa lỗi** → [README.md](README.md) - Phần 10 (Troubleshooting)
- **Viết báo cáo** → [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md) - Phần 4
- **Hiểu code** → Đọc comments trong `src/*.py`
- **Thay đổi corpus** → [QUICKSTART.md](QUICKSTART.md) - Phần "Tùy chỉnh"
- **Tối ưu chi phí** → [ARCHITECTURE.md](ARCHITECTURE.md) - Phần "Tối ưu hóa"

## 📞 Hỗ trợ

### Gặp lỗi?

1. Chạy `python test_setup.py`
2. Đọc [README.md](README.md) - Phần Troubleshooting
3. Tìm kiếm error message trên Google
4. Hỏi trên forum/group

### Không hiểu?

1. Đọc lại [ARCHITECTURE.md](ARCHITECTURE.md)
2. Xem code examples trong `src/`
3. Chạy `notebook.ipynb` từng cell
4. Hỏi giảng viên/trợ giảng

## 🎓 Tài nguyên học thêm

### Về GraphRAG

- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [Knowledge Graphs Paper](https://arxiv.org/abs/2003.02320)

### Về NetworkX

- [NetworkX Tutorial](https://networkx.org/documentation/stable/tutorial.html)
- [Graph Algorithms](https://networkx.org/documentation/stable/reference/algorithms/index.html)

### Về Neo4j

- [Neo4j Getting Started](https://neo4j.com/developer/get-started/)
- [Cypher Query Language](https://neo4j.com/developer/cypher/)

### Về RAG

- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

## ✅ Checklist hoàn thành

- [ ] Đã đọc README.md
- [ ] Đã chạy thành công test_setup.py
- [ ] Đã chạy thành công main.py
- [ ] Đã xem graph_visualization.png
- [ ] Đã hiểu kiến trúc từ ARCHITECTURE.md
- [ ] Đã so sánh GraphRAG vs Flat RAG
- [ ] Đã viết báo cáo
- [ ] Đã chuẩn bị nộp bài theo SUBMISSION_GUIDE.md

## 🎉 Kết luận

Dự án này cung cấp một implementation hoàn chỉnh của GraphRAG system, từ extraction đến evaluation. Hãy đọc kỹ tài liệu, chạy thử, và thử nghiệm với dữ liệu của riêng bạn!

**Chúc bạn thành công! 🚀**

---

**Cập nhật lần cuối**: 2026-05-06
**Phiên bản**: 1.0
