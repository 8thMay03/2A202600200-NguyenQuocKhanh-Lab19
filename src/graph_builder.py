"""
Module xây dựng đồ thị tri thức từ các triples
Hỗ trợ 3 backend: NetworkX, Neo4j, và NodeRAG
"""
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from neo4j import GraphDatabase
import json


class NetworkXGraphBuilder:
    """Xây dựng đồ thị sử dụng NetworkX"""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
    
    def add_triple(self, subject: str, predicate: str, obj: str):
        """Thêm một triple vào đồ thị"""
        self.graph.add_node(subject, type='entity')
        self.graph.add_node(obj, type='entity')
        self.graph.add_edge(subject, obj, relation=predicate)
    
    def add_triples(self, triples: List[Tuple[str, str, str]]):
        """Thêm nhiều triples vào đồ thị"""
        for s, p, o in triples:
            self.add_triple(s, p, o)
    
    def get_neighbors(self, entity: str, max_hops: int = 2) -> List[Tuple[str, str, str]]:
        """
        Lấy tất cả các triples trong phạm vi max_hops từ entity
        
        Args:
            entity: Tên thực thể
            max_hops: Số bước tối đa để duyệt
            
        Returns:
            List các triples liên quan
        """
        if entity not in self.graph:
            return []
        
        # BFS để tìm tất cả nodes trong phạm vi max_hops
        visited_nodes = set()
        current_level = {entity}
        
        for _ in range(max_hops):
            next_level = set()
            for node in current_level:
                if node not in visited_nodes:
                    visited_nodes.add(node)
                    # Thêm cả predecessors và successors
                    next_level.update(self.graph.predecessors(node))
                    next_level.update(self.graph.successors(node))
            current_level = next_level
        
        # Trích xuất tất cả edges giữa các nodes đã visit
        triples = []
        for node in visited_nodes:
            for neighbor in self.graph.successors(node):
                if neighbor in visited_nodes:
                    # Lấy tất cả edges giữa node và neighbor
                    edges = self.graph.get_edge_data(node, neighbor)
                    for edge_data in edges.values():
                        relation = edge_data.get('relation', 'RELATED_TO')
                        triples.append((node, relation, neighbor))
        
        return triples
    
    def visualize(self, output_path: str = "graph_visualization.png", figsize=(20, 15)):
        """Trực quan hóa đồ thị"""
        plt.figure(figsize=figsize)
        
        # Sử dụng spring layout cho đồ thị đẹp hơn
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # Vẽ nodes
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', 
                              node_size=3000, alpha=0.9)
        
        # Vẽ labels
        nx.draw_networkx_labels(self.graph, pos, font_size=8, font_weight='bold')
        
        # Vẽ edges
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, alpha=0.6,
                              connectionstyle='arc3,rad=0.1')
        
        # Vẽ edge labels
        edge_labels = {}
        for u, v, data in self.graph.edges(data=True):
            if (u, v) not in edge_labels:
                edge_labels[(u, v)] = data.get('relation', '')
            else:
                edge_labels[(u, v)] += f"\n{data.get('relation', '')}"
        
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=6)
        
        plt.title("Knowledge Graph Visualization", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Graph visualization saved to {output_path}")
        plt.close()
    
    def get_stats(self) -> dict:
        """Lấy thống kê về đồ thị"""
        return {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "is_connected": nx.is_weakly_connected(self.graph)
        }
    
    def save(self, path: str):
        """Lưu đồ thị ra file"""
        data = nx.node_link_data(self.graph)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self, path: str):
        """Tải đồ thị từ file"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.graph = nx.node_link_graph(data, directed=True, multigraph=True)


class Neo4jGraphBuilder:
    """Xây dựng đồ thị sử dụng Neo4j"""
    
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        """Đóng kết nối"""
        self.driver.close()
    
    def clear_database(self):
        """Xóa toàn bộ database"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
    
    def add_triple(self, subject: str, predicate: str, obj: str):
        """Thêm một triple vào Neo4j"""
        with self.driver.session() as session:
            query = """
            MERGE (s:Entity {name: $subject})
            MERGE (o:Entity {name: $object})
            MERGE (s)-[r:%s]->(o)
            """ % predicate
            
            session.run(query, subject=subject, object=obj)
    
    def add_triples(self, triples: List[Tuple[str, str, str]]):
        """Thêm nhiều triples vào Neo4j"""
        for s, p, o in triples:
            # Normalize predicate để tạo relationship type hợp lệ
            p_normalized = p.replace(' ', '_').replace('-', '_').upper()
            self.add_triple(s, p_normalized, o)
    
    def get_neighbors(self, entity: str, max_hops: int = 2) -> List[Tuple[str, str, str]]:
        """Lấy tất cả các triples trong phạm vi max_hops từ entity"""
        with self.driver.session() as session:
            query = f"""
            MATCH path = (start:Entity {{name: $entity}})-[*1..{max_hops}]-(connected)
            MATCH (n)-[r]->(m)
            WHERE n IN nodes(path) AND m IN nodes(path)
            RETURN n.name as subject, type(r) as predicate, m.name as object
            """
            
            result = session.run(query, entity=entity)
            triples = [(record["subject"], record["predicate"], record["object"]) 
                      for record in result]
            return triples
    
    def get_stats(self) -> dict:
        """Lấy thống kê về đồ thị"""
        with self.driver.session() as session:
            node_count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            edge_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]
            
            return {
                "num_nodes": node_count,
                "num_edges": edge_count
            }


if __name__ == "__main__":
    # Test NetworkX builder
    builder = NetworkXGraphBuilder()
    
    test_triples = [
        ("OpenAI", "FOUNDED_BY", "Sam Altman"),
        ("OpenAI", "FOUNDED_BY", "Elon Musk"),
        ("OpenAI", "FOUNDED_IN", "2015"),
        ("Sam Altman", "CEO_OF", "OpenAI"),
    ]
    
    builder.add_triples(test_triples)
    print("Graph stats:", builder.get_stats())
    
    neighbors = builder.get_neighbors("OpenAI", max_hops=2)
    print(f"\nNeighbors of OpenAI: {len(neighbors)} triples")
    for s, p, o in neighbors:
        print(f"  ({s}, {p}, {o})")
