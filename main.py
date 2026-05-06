"""
Main script: Xây dựng và đánh giá hệ thống GraphRAG
"""
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from entity_extraction import EntityExtractor
from graph_builder import NetworkXGraphBuilder
from graph_rag import GraphRAG
from flat_rag import FlatRAG

load_dotenv()


def build_knowledge_graph(corpus_path: str, output_dir: str = "output"):
    """
    Xây dựng đồ thị tri thức từ corpus
    
    Args:
        corpus_path: Đường dẫn đến file corpus
        output_dir: Thư mục lưu output
    """
    print("="*80)
    print("BƯỚC 1: TRÍCH XUẤT THỰC THỂ VÀ QUAN HỆ")
    print("="*80)
    
    # Khởi tạo extractor
    extractor = EntityExtractor()
    
    # Trích xuất triples
    print(f"\nĐang trích xuất triples từ {corpus_path}...")
    triples = extractor.extract_from_corpus(corpus_path)
    
    # Khử trùng
    print("\nĐang khử trùng lặp...")
    unique_triples = extractor.deduplicate_triples(triples)
    print(f"Triples sau khử trùng: {len(unique_triples)}")
    
    # Lưu triples
    os.makedirs(output_dir, exist_ok=True)
    triples_path = os.path.join(output_dir, "triples.json")
    with open(triples_path, 'w', encoding='utf-8') as f:
        json.dump([{"subject": s, "predicate": p, "object": o} for s, p, o in unique_triples], 
                  f, ensure_ascii=False, indent=2)
    print(f"Đã lưu triples vào {triples_path}")
    
    print("\n" + "="*80)
    print("BƯỚC 2: XÂY DỰNG ĐỒ THỊ TRI THỨC")
    print("="*80)
    
    # Xây dựng đồ thị
    builder = NetworkXGraphBuilder()
    builder.add_triples(unique_triples)
    
    # Thống kê
    stats = builder.get_stats()
    print(f"\nThống kê đồ thị:")
    print(f"  - Số nodes: {stats['num_nodes']}")
    print(f"  - Số edges: {stats['num_edges']}")
    print(f"  - Mật độ: {stats['density']:.4f}")
    print(f"  - Liên thông: {stats['is_connected']}")
    
    # Lưu đồ thị
    graph_path = os.path.join(output_dir, "knowledge_graph.json")
    builder.save(graph_path)
    print(f"\nĐã lưu đồ thị vào {graph_path}")
    
    # Trực quan hóa
    viz_path = os.path.join(output_dir, "graph_visualization.png")
    print(f"\nĐang tạo visualization...")
    builder.visualize(viz_path)
    
    return builder, unique_triples


def setup_flat_rag(corpus_path: str):
    """
    Thiết lập Flat RAG baseline
    
    Args:
        corpus_path: Đường dẫn đến file corpus
    """
    print("\n" + "="*80)
    print("THIẾT LẬP FLAT RAG (BASELINE)")
    print("="*80)
    
    flat_rag = FlatRAG()
    flat_rag.index_corpus(corpus_path)
    
    return flat_rag


def evaluate_systems(graph_rag: GraphRAG, flat_rag: FlatRAG, output_dir: str = "output"):
    """
    Đánh giá và so sánh GraphRAG vs Flat RAG
    
    Args:
        graph_rag: Hệ thống GraphRAG
        flat_rag: Hệ thống Flat RAG
        output_dir: Thư mục lưu kết quả
    """
    print("\n" + "="*80)
    print("BƯỚC 3: ĐÁNH GIÁ VÀ SO SÁNH")
    print("="*80)
    
    # Danh sách câu hỏi benchmark
    questions = [
        "OpenAI được thành lập bởi ai và vào năm nào?",
        "Sam Altman có vai trò gì tại OpenAI?",
        "Elon Musk có liên quan gì đến OpenAI và Tesla?",
        "Microsoft đã đầu tư bao nhiêu vào OpenAI?",
        "Những công ty nào được thành lập bởi Elon Musk?",
        "Google phát triển mô hình AI nào để cạnh tranh với OpenAI?",
        "NVIDIA cung cấp GPU gì cho OpenAI?",
        "Sam Altman từng làm việc ở đâu trước khi gia nhập OpenAI?",
        "Meta phát triển mô hình AI mã nguồn mở nào?",
        "Apple hợp tác với OpenAI để làm gì?",
        "Jensen Huang là CEO của công ty nào?",
        "Y Combinator đã đầu tư vào những công ty nào?",
        "Netflix chuyển sang dịch vụ streaming vào năm nào?",
        "Amazon được thành lập bởi ai và bắt đầu kinh doanh gì?",
        "Tesla được thành lập bởi ai và Elon Musk gia nhập khi nào?",
        "Những người đồng sáng lập Google là ai?",
        "Microsoft phát triển những sản phẩm nào?",
        "Apple được thành lập bởi những ai?",
        "SpaceX có mục tiêu gì?",
        "NVIDIA được thành lập bởi ai và vào năm nào?"
    ]
    
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*80}")
        print(f"Câu hỏi {i}/{len(questions)}: {question}")
        print(f"{'='*80}")
        
        # Test GraphRAG
        print("\n[GraphRAG]")
        graph_result = graph_rag.answer_query(question, max_hops=2, verbose=False)
        print(f"Answer: {graph_result['answer']}")
        
        # Test Flat RAG
        print("\n[Flat RAG]")
        flat_result = flat_rag.answer_query(question, top_k=3, verbose=False)
        print(f"Answer: {flat_result['answer']}")
        
        results.append({
            "question": question,
            "graph_rag": {
                "answer": graph_result['answer'],
                "num_facts": graph_result['num_facts'],
                "entities": graph_result['entities']
            },
            "flat_rag": {
                "answer": flat_result['answer'],
                "num_docs": flat_result['num_docs']
            }
        })
    
    # Lưu kết quả
    results_path = os.path.join(output_dir, "evaluation_results.json")
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"Đã lưu kết quả đánh giá vào {results_path}")
    print(f"{'='*80}")
    
    return results


def main():
    """Main function"""
    print("\n" + "="*80)
    print("HỆ THỐNG GRAPHRAG - TECH COMPANY CORPUS")
    print("="*80)
    print(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Kiểm tra API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  CẢNH BÁO: Chưa thiết lập OPENAI_API_KEY")
        print("Vui lòng tạo file .env và thêm OPENAI_API_KEY=your_key_here")
        return
    
    corpus_path = "data/tech_company_corpus.txt"
    output_dir = "output"
    
    # Bước 1 & 2: Xây dựng Knowledge Graph
    graph_builder, triples = build_knowledge_graph(corpus_path, output_dir)
    
    # Khởi tạo GraphRAG
    graph_rag = GraphRAG(graph_builder)
    
    # Thiết lập Flat RAG
    flat_rag = setup_flat_rag(corpus_path)
    
    # Bước 3: Đánh giá
    results = evaluate_systems(graph_rag, flat_rag, output_dir)
    
    print("\n" + "="*80)
    print("HOÀN THÀNH!")
    print("="*80)
    print(f"\nKết quả được lưu trong thư mục: {output_dir}/")
    print("  - triples.json: Các bộ ba đã trích xuất")
    print("  - knowledge_graph.json: Đồ thị tri thức")
    print("  - graph_visualization.png: Hình ảnh đồ thị")
    print("  - evaluation_results.json: Kết quả đánh giá")


if __name__ == "__main__":
    main()
