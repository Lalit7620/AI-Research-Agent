def build_context(retrieved_chunks):

    context_parts = []

    for chunk in retrieved_chunks:

        context_parts.append(
            chunk["text"]
        )

    return "\n\n".join(context_parts)