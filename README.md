# LAB DAY 19: XÂY DỰNG HỆ THỐNG GRAPHRAG VỚI TECH COMPANY CORPUS

## 1. MỤC TIÊU BÀI HỌC

- Hiểu rõ quy trình trích xuất thực thể (Entity Extraction) và quan hệ (Relation Extraction) từ văn bản thô
- Làm quen với các thư viện quản lý đồ thị: NetworkX, Neo4j và framework mã nguồn mở NodeRAG
- Xây dựng hoàn chỉnh một pipeline GraphRAG: từ lập chỉ mục (Indexing) đến truy vấn đa bước (Multi-hop Querying)
- Đánh giá sự khác biệt về độ chính xác giữa Flat RAG và GraphRAG

## 2. PHẦN 1: NGHIÊN CỨU VÀ CHUẨN BỊ (RESEARCH)

### 2.1. Quy trình xử lý dữ liệu đồ thị

Sinh viên cần trả lời được các câu hỏi:

- **Entity Extraction**: Làm sao để LLM phân biệt được đâu là thực thể (Node) và đâu là thuộc tính?
- **Graph Construction**: Tại sao việc khử trùng lặp (Deduplication) lại quan trọng trong đồ thị?
- **Query Answering**: Sự khác biệt giữa duyệt đồ thị theo chiều rộng (BFS) và tìm kiếm vector thông thường là gì?

### 2.2. Tìm hiểu công cụ

- **NetworkX**: Thư viện Python dùng để nghiên cứu các mạng lưới phức tạp. Phù hợp cho việc tạo prototype nhanh.
- **Neo4j**: Cơ sở dữ liệu đồ thị chuẩn công nghiệp, sử dụng ngôn ngữ truy vấn Cypher.

**Lưu ý**: Dự án này sử dụng NetworkX để xây dựng GraphRAG từ đầu, giúp hiểu rõ cơ chế hoạt động. NodeRAG có thể được thêm vào sau nếu muốn sử dụng framework có sẵn.

## 3. PHẦN 2: ENVIRONMENT SETUP

### Cài đặt thư viện

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv .venv

# Kích hoạt virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Cấu hình API Key

1. Tạo file `.env` từ template:
```bash
cp .env.example .env
```

2. Thêm OpenAI API key vào file `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Cài đặt Neo4j (Tùy chọn)

Nếu muốn sử dụng Neo4j:

```bash
# Sử dụng Docker
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

Hoặc tải Neo4j Desktop từ: https://neo4j.com/download/

## 4. PHẦN 3: HƯỚNG DẪN THỰC HIỆN TỪNG BƯỚC

### Bước 1: Trích xuất thực thể và quan hệ (Indexing)

Sử dụng LLM để đọc bộ dữ liệu "Tech Company Corpus" và chuyển đổi thành các bộ ba (Triples).

**Input**: "OpenAI được thành lập bởi Sam Altman và Elon Musk vào năm 2015."

**Output (Triples)**:
```
(OpenAI, FOUNDED_BY, Sam Altman)
(OpenAI, FOUNDED_BY, Elon Musk)
(OpenAI, FOUNDED_IN, 2015)
```

### Bước 2: Xây dựng đồ thị (Construction)

Sinh viên thực hiện đẩy dữ liệu vào một trong ba công cụ sau:

- **Lựa chọn A (NetworkX)**: Phù hợp để chạy offline trong Notebook
- **Lựa chọn B (Neo4j)**: Khuyên dùng nếu muốn trực quan hóa các mối liên kết bằng mắt thường
- **Lựa chọn C (NodeRAG)**: Sử dụng nếu muốn một giải pháp trọn gói (all-in-one) đã được tối ưu sẵn logic tìm kiếm

### Bước 3: Thực thi truy vấn (Querying)

Viết hàm xử lý truy vấn theo logic:

1. Nhận câu hỏi từ người dùng
2. Trích xuất thực thể chính trong câu hỏi (ví dụ: "Google")
3. Tìm node tương ứng trong đồ thị và duyệt (traverse) các node lân cận trong phạm vi 2-hop
4. Gộp các thông tin tìm được thành một đoạn văn (Textualization) và gửi cho LLM

### Bước 4: So sánh và Đánh giá (Evaluation)

Sinh viên chạy thử câu hỏi phức tạp trên cả hai hệ thống:

- **Flat RAG**: Chỉ dùng ChromaDB/Faiss
- **GraphRAG**: Dùng đồ thị vừa xây dựng

**Yêu cầu**: Ghi lại các trường hợp Flat RAG bị ảo giác nhưng GraphRAG trả lời đúng.

## 5. CHẠY HỆ THỐNG

### Chạy toàn bộ pipeline

```bash
python main.py
```

Script này sẽ:
1. Trích xuất triples từ corpus
2. Xây dựng knowledge graph
3. Tạo visualization
4. Đánh giá cả GraphRAG và Flat RAG trên 20 câu hỏi
5. Lưu kết quả vào thư mục `output/`

### Chạy từng module riêng lẻ

```bash
# Test entity extraction
python src/entity_extraction.py

# Test graph builder
python src/graph_builder.py

# Test GraphRAG
python src/graph_rag.py

# Test Flat RAG
python src/flat_rag.py
```

## 6. CẤU TRÚC DỰ ÁN

```
.
├── data/
│   └── tech_company_corpus.txt    # Dữ liệu corpus
├── src/
│   ├── entity_extraction.py       # Trích xuất thực thể và quan hệ
│   ├── graph_builder.py           # Xây dựng đồ thị (NetworkX, Neo4j)
│   ├── graph_rag.py               # GraphRAG query engine
│   └── flat_rag.py                # Flat RAG baseline
├── output/
│   ├── triples.json               # Các bộ ba đã trích xuất
│   ├── knowledge_graph.json       # Đồ thị tri thức
│   ├── graph_visualization.png    # Hình ảnh đồ thị
│   └── evaluation_results.json    # Kết quả đánh giá
├── main.py                        # Script chính
├── requirements.txt               # Dependencies
├── .env.example                   # Template cho environment variables
└── README.md                      # Tài liệu này
```

## 7. ĐỀ XUẤT CÔNG CỤ (RECOMMENDATIONS)

| Mục tiêu | Tool gợi ý | Lý do |
|----------|-----------|-------|
| Dễ bắt đầu | NetworkX | Đơn giản, dễ hiểu, không cần cấu hình phức tạp |
| Trực quan hóa tốt nhất | Neo4j | Giao diện đồ họa giúp "thấy" được tri thức đang được kết nối như thế nào |
| Nghiên cứu thuật toán | NetworkX | Cho phép can thiệp sâu vào các thuật toán toán học của đồ thị |

## 8. KẾT QUẢ MONG ĐỢI

Sau khi chạy `main.py`, bạn sẽ có:

1. **triples.json**: Danh sách các bộ ba (subject, predicate, object) đã trích xuất
2. **knowledge_graph.json**: Đồ thị tri thức ở dạng JSON
3. **graph_visualization.png**: Hình ảnh trực quan hóa đồ thị
4. **evaluation_results.json**: So sánh kết quả giữa GraphRAG và Flat RAG trên 20 câu hỏi

### Ví dụ kết quả

```json
{
  "question": "Elon Musk có liên quan gì đến OpenAI và Tesla?",
  "graph_rag": {
    "answer": "Elon Musk là đồng sáng lập OpenAI và rời khỏi ban lãnh đạo vào năm 2018. Ông hiện là CEO của Tesla.",
    "num_facts": 15,
    "entities": ["Elon Musk", "OpenAI", "Tesla"]
  },
  "flat_rag": {
    "answer": "Elon Musk là CEO của Tesla.",
    "num_docs": 3
  }
}
```

## 9. DELIVERABLES

Sinh viên nộp báo cáo bao gồm:

1. ✅ **Mã nguồn** (File .py hoặc .ipynb)
2. ✅ **Ảnh chụp màn hình đồ thị tri thức** đã xây dựng (từ Neo4j hoặc Matplotlib)
3. ✅ **Bảng so sánh kết quả 20 câu hỏi benchmark** giữa Flat RAG và GraphRAG
4. ✅ **Phân tích ngắn gọn về chi phí** (Token usage, time) khi xây dựng đồ thị

## 10. TROUBLESHOOTING

### Lỗi: "OpenAI API key not found"
- Đảm bảo đã tạo file `.env` và thêm `OPENAI_API_KEY`
- Kiểm tra API key còn credit

### Lỗi: "Module not found"
- Chạy lại: `pip install -r requirements.txt`
- Đảm bảo đã activate virtual environment

### Neo4j connection failed
- Kiểm tra Neo4j đang chạy: `docker ps` hoặc mở Neo4j Desktop
- Kiểm tra URI, username, password trong `.env`

## 11. TÀI LIỆU THAM KHẢO

- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Neo4j Python Driver](https://neo4j.com/docs/python-manual/current/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 12. LIÊN HỆ VÀ HỖ TRỢ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần Troubleshooting
2. Đọc error message cẩn thận
3. Tìm kiếm trên Stack Overflow hoặc GitHub Issues
4. Liên hệ giảng viên hoặc trợ giảng

---

**Chúc các bạn thành công với bài lab! 🚀**
