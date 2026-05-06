"""
Module Flat RAG: Truy vấn vector database để trả lời câu hỏi (baseline)
"""
import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()


class FlatRAG:
    """Hệ thống Flat RAG sử dụng ChromaDB"""
    
    def __init__(self, collection_name: str = "tech_corpus", api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        # Khởi tạo ChromaDB
        self.chroma_client = chromadb.Client()
        
        # Sử dụng OpenAI embedding function
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        # Tạo hoặc lấy collection
        try:
            self.collection = self.chroma_client.get_collection(
                name=collection_name,
                embedding_function=openai_ef
            )
        except:
            self.collection = self.chroma_client.create_collection(
                name=collection_name,
                embedding_function=openai_ef
            )
    
    def index_corpus(self, corpus_path: str):
        """
        Đánh chỉ mục corpus vào vector database
        
        Args:
            corpus_path: Đường dẫn đến file corpus
        """
        with open(corpus_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Chia văn bản thành các đoạn
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Thêm vào ChromaDB
        ids = [f"doc_{i}" for i in range(len(paragraphs))]
        
        self.collection.add(
            documents=paragraphs,
            ids=ids
        )
        
        print(f"Indexed {len(paragraphs)} paragraphs into ChromaDB")
    
    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """
        Truy vấn vector database để lấy context
        
        Args:
            query: Câu hỏi của người dùng
            top_k: Số lượng documents cần lấy
            
        Returns:
            Context dưới dạng văn bản
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        documents = results['documents'][0]
        context = "\n\n".join(documents)
        return context
    
    def answer_query(self, query: str, top_k: int = 5, verbose: bool = True) -> dict:
        """
        Trả lời câu hỏi sử dụng Flat RAG
        
        Args:
            query: Câu hỏi của người dùng
            top_k: Số lượng documents cần retrieve
            verbose: In thông tin debug
            
        Returns:
            Dict chứa answer, context, và metadata
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print(f"{'='*60}")
        
        # Retrieve context
        context = self.retrieve_context(query, top_k=top_k)
        
        if verbose:
            print(f"\nRetrieved context ({top_k} documents):")
            print(context[:500] + "..." if len(context) > 500 else context)
        
        # Generate answer
        prompt = f"""
Dựa trên các thông tin sau, hãy trả lời câu hỏi một cách chính xác và đầy đủ.

Thông tin:
{context}

Câu hỏi: {query}

Hướng dẫn:
- Chỉ sử dụng thông tin được cung cấp
- Nếu không có đủ thông tin, hãy nói rõ điều đó
- Trả lời ngắn gọn, súc tích nhưng đầy đủ

Trả lời:
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
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
                "context": context,
                "answer": answer,
                "num_docs": top_k
            }
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return {
                "query": query,
                "context": context,
                "answer": f"Error: {str(e)}",
                "num_docs": top_k
            }


if __name__ == "__main__":
    # Test Flat RAG
    rag = FlatRAG()
    
    # Index corpus
    rag.index_corpus("../data/tech_company_corpus.txt")
    
    # Test query
    result = rag.answer_query("OpenAI được thành lập bởi ai?")
    print(f"\nFinal answer: {result['answer']}")
