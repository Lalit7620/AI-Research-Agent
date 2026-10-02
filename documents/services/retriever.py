from .embeddings import embed_texts
from .vector_store import collection

def retrieve(query,user_id,top_k=3):
    query_embedding=embed_texts([query])
    
    results=collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        where={
            "user_id":user_id
        }
    )
    
    retrieved_chunks = []

    for index in range(len(results["ids"][0])):

        retrieved_chunks.append({
            "text": results["documents"][0][index],
            "document_id": results["metadatas"][0][index]["document_id"],
            "page_number": results["metadatas"][0][index]["page_number"],
            "distance": results["distances"][0][index]
        })

    return retrieved_chunks