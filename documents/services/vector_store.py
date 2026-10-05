import chromadb

from django.conf import settings


client=chromadb.PersistentClient(
    path=str(settings.CHROMA_DB_PATH)
)

collection=client.get_or_create_collection(
    name="documents"
)

def add_chunks(document_id,user_id,chunks,embeddings):
    ids=[
        f"doc_{document_id}_chunk_{index}"
        for index in range(len(chunks))
    ]
    
    documents=[
        chunk["text"]
        for chunk in chunks
    ]
    
    metadatas=[
        {
            "document_id":document_id,
            "user_id":user_id,
            "page_number":chunk["page_number"]
        }
        for chunk in chunks
    ]
    
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )
    
def delete_document_chunks(document_id):
    collection.delete(
        where={
            "document_id":document_id
        }
    )