# 🏗️ KIẾN TRÚC HỆ THỐNG GRAPHRAG

Tài liệu này mô tả chi tiết kiến trúc và luồng hoạt động của hệ thống GraphRAG.

## 📐 Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────────┐
│                    TECH COMPANY CORPUS                       │
│                    (Raw Text Data)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              ENTITY & RELATION EXTRACTION                    │
│                  (entity_extraction.py)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  LLM (GPT-4o-mini)                                   │   │
│  │  Input: "OpenAI được thành lập bởi Sam Altman..."   │   │
│  │  Output: [(OpenAI, FOUNDED_BY, Sam Altman), ...]    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 KNOWLEDGE GRAPH BUILDER                      │
│                   (graph_builder.py)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  NetworkX MultiDiGraph                               │   │
│  │  Nodes: Entities (OpenAI, Sam Altman, ...)          │   │
│  │  Edges: Relations (FOUNDED_BY, CEO_OF, ...)         │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────┬───────────────────────────────┬────────────────┘
             │                               │
             ▼                               ▼
┌────────────────────────┐      ┌───────────────────────────┐
│   GRAPHRAG SYSTEM      │      │   FLAT RAG SYSTEM         │
│   (graph_rag.py)       │      │   (flat_rag.py)           │
│                        │      │                           │
│  1. Extract entities   │      │  1. Embed paragraphs      │
│  2. BFS traversal      │      │  2. Vector search         │
│  3. Gather context     │      │  3. Retrieve top-k        │
│  4. LLM generation     │      │  4. LLM generation        │
└────────────┬───────────┘      └───────────┬───────────────┘
             │                               │
             └───────────┬───────────────────┘
                         ▼
              ┌─────────────────────┐
              │   EVALUATION        │
              │   (main.py)         │
              │                     │
              │  Compare answers    │
              │  on 20 questions    │
              └─────────────────────┘
```

## 🔍 Chi tiết các module

### 1. Entity Extraction (`src/entity_extraction.py`)

**Chức năng**: Trích xuất thực thể và quan hệ từ văn bản thô.

**Input**: 
```
"OpenAI được thành lập bởi Sam Altman và Elon Musk vào năm 2015."
```

**Output**:
```python
[
    ("OpenAI", "FOUNDED_BY", "Sam Altman"),
    ("OpenAI", "FOUNDED_BY", "Elon Musk"),
    ("OpenAI", "FOUNDED_IN", "2015")
]
```

**Quy trình**:
1. Chia corpus thành các đoạn văn
2. Với mỗi đoạn, gọi LLM để trích xuất triples
3. Khử trùng lặp các triples
4. Normalize format (uppercase predicates, strip whitespace)

**Prompt Engineering**:
- Yêu cầu LLM trả về JSON format
- Định nghĩa rõ subject, predicate, object
- Sử dụng tiếng Anh cho predicates để consistency

### 2. Graph Builder (`src/graph_builder.py`)

**Chức năng**: Xây dựng và quản lý đồ thị tri thức.

**Cấu trúc đồ thị**:
```python
# NetworkX MultiDiGraph
graph = {
    "nodes": [
        {"id": "OpenAI", "type": "entity"},
        {"id": "Sam Altman", "type": "entity"},
        ...
    ],
    "edges": [
        {"source": "OpenAI", "target": "Sam Altman", "relation": "FOUNDED_BY"},
        ...
    ]
}
```

**Các phương thức chính**:
- `add_triple(s, p, o)`: Thêm một triple vào đồ thị
- `get_neighbors(entity, max_hops)`: Duyệt đồ thị theo BFS
- `visualize()`: Tạo hình ảnh đồ thị
- `get_stats()`: Thống kê nodes, edges, density

**Thuật toán BFS (Breadth-First Search)**:
```python
def get_neighbors(entity, max_hops=2):
    visited = set()
    current_level = {entity}
    
    for hop in range(max_hops):
        next_level = set()
        for node in current_level:
            visited.add(node)
            # Thêm predecessors và successors
            next_level.update(graph.predecessors(node))
            next_level.update(graph.successors(node))
        current_level = next_level
    
    return extract_edges(visited)
```

### 3. GraphRAG (`src/graph_rag.py`)

**Chức năng**: Trả lời câu hỏi dựa trên đồ thị tri thức.

**Quy trình truy vấn**:

```
User Query: "Elon Musk có liên quan gì đến OpenAI và Tesla?"
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 1: Entity Extraction               │
│ Entities: ["Elon Musk", "OpenAI",       │
│            "Tesla"]                      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 2: Graph Traversal (BFS)           │
│ From "Elon Musk" (2 hops):              │
│   - Elon Musk → FOUNDED → OpenAI        │
│   - Elon Musk → CEO_OF → Tesla          │
│   - Elon Musk → LEFT → OpenAI (2018)    │
│   - ...                                  │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 3: Context Textualization          │
│ "- Elon Musk founded OpenAI             │
│  - Elon Musk is CEO of Tesla            │
│  - Elon Musk left OpenAI in 2018        │
│  - ..."                                  │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 4: LLM Generation                  │
│ Answer: "Elon Musk là đồng sáng lập     │
│ OpenAI và rời khỏi ban lãnh đạo vào     │
│ năm 2018. Ông hiện là CEO của Tesla."   │
└─────────────────────────────────────────┘
```

**Ưu điểm**:
- ✅ Multi-hop reasoning: Kết nối thông tin qua nhiều bước
- ✅ Structured context: Thông tin có cấu trúc rõ ràng
- ✅ Explainable: Có thể trace nguồn gốc thông tin

**Nhược điểm**:
- ❌ Chi phí cao: Nhiều API calls
- ❌ Phụ thuộc extraction quality
- ❌ Phức tạp hơn Flat RAG

### 4. Flat RAG (`src/flat_rag.py`)

**Chức năng**: Baseline sử dụng vector search (ChromaDB).

**Quy trình truy vấn**:

```
User Query: "Elon Musk có liên quan gì đến OpenAI và Tesla?"
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 1: Embed Query                     │
│ Vector: [0.123, -0.456, 0.789, ...]     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 2: Vector Search (Cosine)          │
│ Top 3 paragraphs:                        │
│   1. "Elon Musk rời khỏi OpenAI..."     │
│   2. "Tesla được thành lập..."          │
│   3. "SpaceX được thành lập..."         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Step 3: LLM Generation                  │
│ Answer: "Elon Musk là CEO của Tesla."   │
│ (Thiếu thông tin về OpenAI)             │
└─────────────────────────────────────────┘
```

**Ưu điểm**:
- ✅ Đơn giản, dễ implement
- ✅ Chi phí thấp
- ✅ Nhanh

**Nhược điểm**:
- ❌ Không có multi-hop reasoning
- ❌ Có thể miss thông tin quan trọng
- ❌ Phụ thuộc vào semantic similarity

## 🔄 Luồng dữ liệu chính

### Indexing Phase (Offline)

```
Raw Text → Entity Extraction → Triples → Graph Construction → Knowledge Graph
```

**Chi phí**: ~$0.10 - $0.20 (one-time)

### Query Phase (Online)

**GraphRAG**:
```
Query → Entity Extraction → Graph Traversal → Context Gathering → LLM → Answer
```
**Chi phí**: ~$0.005 - $0.01 per query

**Flat RAG**:
```
Query → Vector Search → Context Retrieval → LLM → Answer
```
**Chi phí**: ~$0.003 - $0.005 per query

## 📊 So sánh GraphRAG vs Flat RAG

| Tiêu chí | GraphRAG | Flat RAG |
|----------|----------|----------|
| **Độ chính xác** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Multi-hop** | ✅ Có | ❌ Không |
| **Chi phí** | 💰💰💰 | 💰 |
| **Tốc độ** | 🐢 Chậm | 🚀 Nhanh |
| **Độ phức tạp** | 🔧🔧🔧 | 🔧 |
| **Explainability** | ✅ Cao | ⚠️ Trung bình |
| **Scalability** | ⚠️ Trung bình | ✅ Cao |

## 🎯 Khi nào dùng GraphRAG?

✅ **Nên dùng khi**:
- Dữ liệu có nhiều mối quan hệ phức tạp
- Cần trả lời câu hỏi multi-hop
- Cần explainability cao
- Domain knowledge rõ ràng (entities, relations)
- Độ chính xác quan trọng hơn chi phí

❌ **Không nên dùng khi**:
- Dữ liệu đơn giản, ít mối quan hệ
- Cần tốc độ cao, chi phí thấp
- Câu hỏi đơn giản, không cần multi-hop
- Dữ liệu thay đổi liên tục (khó maintain graph)

## 🔧 Tối ưu hóa

### 1. Giảm chi phí

- Sử dụng model nhỏ hơn cho extraction (gpt-3.5-turbo)
- Cache kết quả extraction
- Batch processing cho nhiều paragraphs

### 2. Tăng độ chính xác

- Fine-tune prompt cho extraction
- Thêm validation step cho triples
- Sử dụng entity linking/resolution

### 3. Tăng tốc độ

- Index đồ thị vào Neo4j
- Cache kết quả truy vấn phổ biến
- Giới hạn max_hops hợp lý

## 📚 Tài liệu tham khảo

- [NetworkX Documentation](https://networkx.org/)
- [Neo4j Graph Database](https://neo4j.com/)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
- [Knowledge Graphs Paper](https://arxiv.org/abs/2003.02320)

---

**Tác giả**: Lab Day 19 - GraphRAG System
**Ngày cập nhật**: 2026-05-06
