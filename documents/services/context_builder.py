def build_context(retrieved_chunks):

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            f"[Document {chunk['document_id']} - Page {chunk['page_number']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)