from .pdf_loader import extract_text_from_pdf
from .chunker import chunk_pages
from .embeddings import embed_texts
from .vector_store import add_chunks


def ingest_document(document):
    pages=extract_text_from_pdf(document.file.path)
    
    chunks=chunk_pages(pages)
    
    embeddings=embed_texts(
        [chunk["text"] for chunk in chunks]
    )
    
    add_chunks(
        document.id,
        document.user.id,
        chunks,
        embeddings
    )