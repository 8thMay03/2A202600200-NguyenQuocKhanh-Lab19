"""
Module trích xuất thực thể và quan hệ từ văn bản sử dụng LLM
"""
import os
from typing import List, Dict, Tuple
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

class EntityExtractor:
    """Trích xuất thực thể và quan hệ từ văn bản"""
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
    def extract_triples(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Trích xuất các bộ ba (subject, predicate, object) từ văn bản
        
        Args:
            text: Văn bản đầu vào
            
        Returns:
            List các tuple (subject, predicate, object)
        """
        prompt = f"""
Bạn là một chuyên gia trích xuất tri thức từ văn bản.
Nhiệm vụ: Trích xuất tất cả các mối quan hệ từ văn bản dưới dạng bộ ba (subject, predicate, object).

Quy tắc:
1. Subject và Object phải là thực thể cụ thể (người, tổ chức, sản phẩm, địa điểm, thời gian)
2. Predicate mô tả mối quan hệ giữa subject và object (FOUNDED_BY, FOUNDED_IN, CEO_OF, INVESTED_IN, etc.)
3. Sử dụng tiếng Anh cho predicate, viết hoa và dùng dấu gạch dưới
4. Trích xuất càng nhiều quan hệ càng tốt, kể cả quan hệ ngầm định

Văn bản:
{text}

Trả về kết quả dưới dạng JSON array với format:
[
    {{"subject": "...", "predicate": "...", "object": "..."}},
    ...
]

Chỉ trả về JSON, không giải thích thêm.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a knowledge extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()
                
            triples_data = json.loads(content)
            
            # Convert to tuple format
            triples = [
                (item["subject"], item["predicate"], item["object"])
                for item in triples_data
            ]
            
            return triples
            
        except Exception as e:
            print(f"Error extracting triples: {e}")
            return []
    
    def extract_from_corpus(self, corpus_path: str) -> List[Tuple[str, str, str]]:
        """
        Trích xuất triples từ toàn bộ corpus
        
        Args:
            corpus_path: Đường dẫn đến file corpus
            
        Returns:
            List tất cả các triples
        """
        with open(corpus_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Chia văn bản thành các đoạn nhỏ
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        all_triples = []
        for i, paragraph in enumerate(paragraphs):
            print(f"Processing paragraph {i+1}/{len(paragraphs)}...")
            triples = self.extract_triples(paragraph)
            all_triples.extend(triples)
            print(f"  Extracted {len(triples)} triples")
        
        print(f"\nTotal triples extracted: {len(all_triples)}")
        return all_triples
    
    def deduplicate_triples(self, triples: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        """
        Khử trùng lặp các triples
        
        Args:
            triples: List các triples
            
        Returns:
            List các triples đã khử trùng
        """
        # Normalize và khử trùng
        unique_triples = set()
        for s, p, o in triples:
            # Normalize: strip whitespace và lowercase cho so sánh
            normalized = (s.strip(), p.strip().upper(), o.strip())
            unique_triples.add(normalized)
        
        return list(unique_triples)


if __name__ == "__main__":
    # Test extraction
    extractor = EntityExtractor()
    
    test_text = "OpenAI được thành lập bởi Sam Altman và Elon Musk vào năm 2015."
    triples = extractor.extract_triples(test_text)
    
    print("Extracted triples:")
    for s, p, o in triples:
        print(f"  ({s}, {p}, {o})")
