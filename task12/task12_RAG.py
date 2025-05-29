import os
from langchain_community.document_loaders import TextLoader, CSVLoader, PyMuPDFLoader

def load_all_documents_from_dir(directory):
    all_docs = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".txt") or filename.endswith(".md"):
            loader = TextLoader(file_path, encoding='utf-8')
        elif filename.endswith(".csv"):
            loader = CSVLoader(file_path, encoding='utf-8')
        elif filename.endswith(".pdf"):
            loader = PyMuPDFLoader(file_path)
        else:
            continue  # 忽略不支持的格式

        docs = loader.load()
        all_docs.extend(docs)

    return all_docs