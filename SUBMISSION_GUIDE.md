# 📝 HƯỚNG DẪN NỘP BÀI LAB 19

## ✅ Checklist trước khi nộp

- [ ] Đã chạy thành công `python main.py`
- [ ] Có file `output/graph_visualization.png`
- [ ] Có file `output/evaluation_results.json`
- [ ] Đã viết báo cáo phân tích
- [ ] Code có comments đầy đủ
- [ ] Đã test trên ít nhất 20 câu hỏi

## 📦 Nội dung nộp bài

### 1. Mã nguồn (Required)

Nộp toàn bộ thư mục dự án, bao gồm:

```
Lab19_GraphRAG/
├── src/
│   ├── entity_extraction.py
│   ├── graph_builder.py
│   ├── graph_rag.py
│   └── flat_rag.py
├── data/
│   └── tech_company_corpus.txt
├── output/
│   ├── triples.json
│   ├── knowledge_graph.json
│   ├── graph_visualization.png
│   └── evaluation_results.json
├── main.py
├── requirements.txt
├── README.md
└── REPORT.md (báo cáo của bạn)
```

**Lưu ý**: 
- ❌ KHÔNG nộp file `.env` (chứa API key)
- ❌ KHÔNG nộp thư mục `.venv/` hoặc `__pycache__/`
- ✅ Nộp file `.env.example` để hướng dẫn

### 2. Ảnh chụp màn hình (Required)

**a) Đồ thị tri thức** (`output/graph_visualization.png`)
- Phải rõ ràng, dễ đọc
- Hiển thị đầy đủ nodes và edges
- Có thể zoom in để xem chi tiết

**b) Kết quả chạy chương trình**
- Screenshot terminal khi chạy `python main.py`
- Hiển thị quá trình extraction và evaluation
- Thời gian chạy và số lượng triples

**c) So sánh kết quả** (Optional nhưng khuyến khích)
- Bảng so sánh GraphRAG vs Flat RAG
- Highlight các trường hợp GraphRAG tốt hơn

### 3. Bảng so sánh 20 câu hỏi (Required)

Tạo file `COMPARISON_TABLE.md`:

```markdown
# So sánh GraphRAG vs Flat RAG

## Tổng quan
- Tổng số câu hỏi: 20
- GraphRAG đúng: X/20
- Flat RAG đúng: Y/20

## Chi tiết từng câu hỏi

| # | Câu hỏi | GraphRAG | Flat RAG | Winner |
|---|---------|----------|----------|--------|
| 1 | OpenAI được thành lập bởi ai? | ✅ Đúng | ✅ Đúng | Tie |
| 2 | Elon Musk có liên quan gì đến OpenAI và Tesla? | ✅ Đúng | ❌ Thiếu info | GraphRAG |
| ... | ... | ... | ... | ... |

## Phân tích

### Trường hợp GraphRAG tốt hơn:
1. Câu hỏi 2: Multi-hop reasoning
2. Câu hỏi 5: Kết nối nhiều entities
...

### Trường hợp Flat RAG tốt hơn:
1. Câu hỏi X: Thông tin trong 1 paragraph
...

### Trường hợp cả hai đều sai:
1. Câu hỏi Y: Thông tin không có trong corpus
...
```

### 4. Báo cáo phân tích (Required)

Tạo file `REPORT.md` với các phần sau:

#### a) Tóm tắt (Executive Summary)
- Mục tiêu bài lab
- Kết quả chính
- Kết luận

#### b) Phương pháp (Methodology)
- Mô tả quy trình extraction
- Thuật toán xây dựng đồ thị
- Cách thức truy vấn

#### c) Kết quả (Results)
- Thống kê đồ thị (số nodes, edges, density)
- Kết quả đánh giá 20 câu hỏi
- So sánh GraphRAG vs Flat RAG

#### d) Phân tích chi phí (Cost Analysis)
- Token usage cho extraction
- Token usage cho querying
- Tổng chi phí ước tính
- Thời gian chạy

**Template**:

```markdown
# BÁO CÁO LAB 19: XÂY DỰNG HỆ THỐNG GRAPHRAG

## 1. Tóm tắt

Bài lab này xây dựng hệ thống GraphRAG để trả lời câu hỏi về các công ty công nghệ...

## 2. Phương pháp

### 2.1. Entity Extraction
- Sử dụng GPT-4o-mini
- Prompt engineering: ...
- Khử trùng lặp: ...

### 2.2. Graph Construction
- Thư viện: NetworkX
- Cấu trúc: MultiDiGraph
- Số nodes: X
- Số edges: Y

### 2.3. Query Processing
- Thuật toán: BFS
- Max hops: 2
- Context gathering: ...

## 3. Kết quả

### 3.1. Thống kê đồ thị
- Số nodes: X
- Số edges: Y
- Mật độ: Z
- Liên thông: Có/Không

### 3.2. Đánh giá
- GraphRAG accuracy: X%
- Flat RAG accuracy: Y%
- Improvement: Z%

### 3.3. Ví dụ cụ thể

**Câu hỏi**: "Elon Musk có liên quan gì đến OpenAI và Tesla?"

**GraphRAG**: 
- Answer: "Elon Musk là đồng sáng lập OpenAI và rời khỏi ban lãnh đạo vào năm 2018. Ông hiện là CEO của Tesla."
- Facts used: 15
- Correct: ✅

**Flat RAG**:
- Answer: "Elon Musk là CEO của Tesla."
- Docs used: 3
- Correct: ⚠️ (Thiếu thông tin về OpenAI)

## 4. Phân tích chi phí

### 4.1. Token Usage
- Extraction phase: X tokens (~$Y)
- Query phase (20 questions): Z tokens (~$W)
- Total: ~$T

### 4.2. Thời gian
- Extraction: X phút
- Graph construction: Y giây
- Query (average): Z giây/câu

## 5. Thảo luận

### 5.1. Ưu điểm của GraphRAG
1. Multi-hop reasoning
2. Structured knowledge
3. Explainable

### 5.2. Nhược điểm
1. Chi phí cao hơn
2. Phức tạp hơn
3. Phụ thuộc extraction quality

### 5.3. Khi nào nên dùng GraphRAG?
- Dữ liệu có nhiều mối quan hệ
- Cần multi-hop reasoning
- Độ chính xác quan trọng

## 6. Kết luận

GraphRAG cho kết quả tốt hơn Flat RAG trong các câu hỏi phức tạp...

## 7. Tài liệu tham khảo

1. NetworkX Documentation
2. Microsoft GraphRAG
3. ...
```

## 📤 Cách nộp bài

### Option 1: Nộp qua GitHub (Khuyến nghị)

```bash
# 1. Tạo repository
git init
git add .
git commit -m "Lab 19: GraphRAG System"

# 2. Push lên GitHub
git remote add origin https://github.com/yourusername/lab19-graphrag.git
git push -u origin main

# 3. Nộp link GitHub
```

### Option 2: Nộp file ZIP

```bash
# 1. Xóa các file không cần thiết
rm -rf .venv __pycache__ .env

# 2. Tạo ZIP
# Windows: Right-click → Send to → Compressed folder
# Linux/Mac: zip -r Lab19_GraphRAG.zip .

# 3. Upload lên hệ thống nộp bài
```

## 🎯 Tiêu chí chấm điểm (Tham khảo)

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Code hoạt động** | 30% | Chạy được, không lỗi |
| **Kết quả đúng** | 20% | Extraction và query chính xác |
| **Visualization** | 15% | Đồ thị rõ ràng, đẹp |
| **So sánh** | 15% | Bảng so sánh đầy đủ, chi tiết |
| **Báo cáo** | 15% | Phân tích sâu, có insight |
| **Code quality** | 5% | Clean code, comments |

## ⚠️ Lưu ý quan trọng

1. **KHÔNG** commit file `.env` chứa API key
2. **KHÔNG** copy code từ bạn khác
3. **PHẢI** chạy thử trước khi nộp
4. **PHẢI** có ảnh chụp màn hình
5. **NÊN** viết báo cáo bằng tiếng Việt (trừ khi yêu cầu khác)

## 🆘 Câu hỏi thường gặp

**Q: Tôi có thể thay đổi corpus không?**
A: Có, nhưng phải giữ format tương tự và có ít nhất 15-20 đoạn văn.

**Q: Phải test đúng 20 câu hỏi không?**
A: Tối thiểu 20 câu. Có thể test nhiều hơn để có kết quả tốt hơn.

**Q: Có thể dùng model khác thay GPT-4o-mini không?**
A: Có, nhưng phải ghi rõ trong báo cáo và giải thích lý do.

**Q: Nếu không có đủ tiền cho OpenAI API thì sao?**
A: Liên hệ giảng viên để được hỗ trợ hoặc dùng free tier (có giới hạn).

**Q: Có cần deploy lên server không?**
A: Không bắt buộc. Chạy local và nộp code + kết quả là đủ.

## 📞 Liên hệ hỗ trợ

Nếu gặp vấn đề:
1. Đọc kỹ `README.md` và `QUICKSTART.md`
2. Chạy `python test_setup.py` để debug
3. Tìm kiếm lỗi trên Google/Stack Overflow
4. Hỏi trên forum/group của lớp
5. Liên hệ giảng viên/trợ giảng

---

**Chúc bạn hoàn thành tốt bài lab! 🎓**
