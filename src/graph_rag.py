"""
Module GraphRAG: Truy vấn đồ thị tri thức để trả lời câu hỏi
"""
import os
from typing import List, Tuple
from openai import OpenAI
from dotenv import load_dotenv
from graph_builder import NetworkXGraphBuilder

load_dotenv()


class GraphRAG:
    """Hệ thống GraphRAG để trả lời câu hỏi dựa trên đồ thị tri thức"""
    
    def __init__(self, graph_builder: NetworkXGraphBuilder, api_key: str = None):
        self.graph = graph_builder
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    
    def extract_entities_from_query(self, query: str) -> List[str]:
        """
        Trích xuất các thực thể chính từ câu hỏi
        
        Args:
            query: Câu hỏi của người dùng
            
        Returns:
            List các thực thể được nhắc đến
        """
        prompt = f"""
Trích xuất tất cả các thực thể (tên người, tổ chức, sản phẩm) từ câu hỏi sau.
Chỉ trả về tên thực thể, mỗi thực thể trên một dòng.

Câu hỏi: {query}

Thực thể:
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an entity extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            entities = [e.strip() for e in content.split('\n') if e.strip()]
            return entities
            
        except Exception as e:
            print(f"Error extracting entities: {e}")
            return []
    
    def gather_context(self, entities: List[str], max_hops: int = 2) -> str:
        """
        Thu thập context từ đồ thị dựa trên các thực thể
        
        Args:
            entities: List các thực thể cần tìm
            max_hops: Số bước tối đa để duyệt đồ thị
            
        Returns:
            Context dưới dạng văn bản
        """
        all_triples = []
        
        for entity in entities:
            triples = self.graph.get_neighbors(entity, max_hops=max_hops)
            all_triples.extend(triples)
        
        # Khử trùng
        unique_triples = list(set(all_triples))
        
        # Chuyển đổi thành văn bản
        context_lines = []
        for s, p, o in unique_triples:
            # Format predicate thành dạng dễ đọc
            p_readable = p.replace('_', ' ').lower()
            context_lines.append(f"- {s} {p_readable} {o}")
        
        context = "\n".join(context_lines)
        return context
    
    def answer_query(self, query: str, max_hops: int = 2, verbose: bool = True) -> dict:
        """
        Trả lời câu hỏi sử dụng GraphRAG
        
        Args:
            query: Câu hỏi của người dùng
            max_hops: Số bước tối đa để duyệt đồ thị
            verbose: In thông tin debug
            
        Returns:
            Dict chứa answer, context, và metadata
        """
        # Bước 1: Trích xuất thực thể từ câu hỏi
        if verbose:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print(f"{'='*60}")
        
        entities = self.extract_entities_from_query(query)
        if verbose:
            print(f"\nExtracted entities: {entities}")
        
        # Bước 2: Thu thập context từ đồ thị
        context = self.gather_context(entities, max_hops=max_hops)
        if verbose:
            print(f"\nGathered context ({len(context.split(chr(10)))} facts):")
            print(context[:500] + "..." if len(context) > 500 else context)
        
        # Bước 3: Gửi context và câu hỏi cho LLM
        prompt = f"""
Dựa trên các thông tin sau từ đồ thị tri thức, hãy trả lời câu hỏi một cách chính xác và đầy đủ.

Thông tin từ đồ thị:
{context}

Câu hỏi: {query}

Hướng dẫn:
- Chỉ sử dụng thông tin từ đồ thị tri thức được cung cấp
- Nếu không có đủ thông tin, hãy nói rõ điều đó
- Trả lời ngắn gọn, súc tích nhưng đầy đủ
- Trích dẫn các thông tin cụ thể từ đồ thị

Trả lời:
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on knowledge graph data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            answer = response.choices[0].message.content.strip()
            
            if verbose:
                print(f"\nAnswer: {answer}")
                print(f"{'='*60}\n")
            
            return {
                "query": query,
                "entities": entities,
                "context": context,
                "answer": answer,
                "num_facts": len(context.split('\n')),
                "max_hops": max_hops
            }
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return {
                "query": query,
                "entities": entities,
                "context": context,
                "answer": f"Error: {str(e)}",
                "num_facts": 0,
                "max_hops": max_hops
            }


if __name__ == "__main__":
    # Test GraphRAG
    from entity_extraction import EntityExtractor
    
    # Build a simple graph
    builder = NetworkXGraphBuilder()
    test_triples = [
        ("OpenAI", "FOUNDED_BY", "Sam Altman"),
        ("OpenAI", "FOUNDED_BY", "Elon Musk"),
        ("OpenAI", "FOUNDED_IN", "2015"),
        ("Sam Altman", "CEO_OF", "OpenAI"),
        ("Sam Altman", "FORMER_PRESIDENT_OF", "Y Combinator"),
    ]
    builder.add_triples(test_triples)
    
    # Test query
    rag = GraphRAG(builder)
    result = rag.answer_query("OpenAI được thành lập bởi ai?")
    print(f"\nFinal answer: {result['answer']}")
