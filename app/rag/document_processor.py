from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunk_documents(documents, chunk_size=1000, chunk_overlap=150):
    chunks = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).split_documents(documents)
    for i, chunk in enumerate(chunks): chunk.metadata["chunk_index"] = i
    return chunks

