from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.llm import embeddings,model
from app.services.video_retrival import get_video_id,context_retival
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever,EnsembleRetriever
#build documents by chunking the transcript
def build_docs(url: str):
    video_id = get_video_id(url)
    transcript = context_retival(video_id)

    docs = [
        Document(
            page_content=chunk["text"],
            metadata={
                "start_time": chunk["start"],
                "end_time": chunk["end"],
                "video_id": video_id
            }
        )
        for chunk in transcript
    ]

    return docs, video_id

#vectore store and retriver for semantic
def semantic_retriever(url: str, top_k=10):
    docs, video_id = build_docs(url)

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": top_k}
    )

    return retriever

    
#bm25 and retriver for word similarity
def word_retriever(url: str, top_k=10):
    docs, video_id = build_docs(url)

    filtered_docs = [
        doc for doc in docs
        if doc.metadata["video_id"] == video_id
    ]

    bm25 = BM25Retriever.from_documents(filtered_docs)
    bm25.k = top_k

    return bm25


#Hybrid Retriver for semantic and word similarity

def hybrid_search(url:str,top_k=10):
    semantic=semantic_retriever(url,top_k)
    word=word_retriever(url,top_k)
    ensemble=EnsembleRetriever(
        retrievers=[semantic,word],
        weights=[0.7,0.3]
    )
    return ensemble