from typing import Generator

from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings
from unstructured.partition.pdf import partition_pdf


from ..config import Config
from ..template import TEMPLATE


class Engine:
    def __init__(self) -> None:
        self.__vectorstore = Chroma(
            embedding_function=OllamaEmbeddings(model=Config.model_embed),
            persist_directory=Config.vectorstore_path,
        )
        self.__chain = (
            TEMPLATE
            | ChatOllama(model=Config.model_chat, temperature=0.8)
            | StrOutputParser()
        )

    async def ask(self, query: str) -> Generator[str, None, None]:
        retrieved = await self.__vectorstore.asimilarity_search_with_relevance_scores(
            query=query, k=10, score_threshold=0.3
        )
        input = {
            "context": [
                SystemMessage(content=f"<context_{i}>{x[0].page_content}</context_{i}>")
                for i, x in enumerate(retrieved, start=1)
            ],
            "question": [HumanMessage(content=f"<question>{query}</question>")],
        }
        return self.__chain.astream(input=input), retrieved


class DataManager:
    def __init__(self) -> None:
        self.__vectorstore = Chroma(
            embedding_function=OllamaEmbeddings(model=Config.model_embed),
            persist_directory=Config.vectorstore_path,
        )

    async def vectorize_and_add(self, path: str) -> None:
        chunks = partition_pdf(
            filename=path,
            chunking_strategy="by_title",
            max_characters=3000,
            combine_text_under_n_chars=1000,
            new_after_n_chars=2500,
        )
        docs = [
            Document(
                page_content=x.text,
                metadata={
                    "page": x.metadata.page_number,
                    "filename": x.metadata.filename,
                },
            )
            for x in chunks
        ]
        await self.__vectorstore.aadd_documents(docs)
