from typing import Generator

from langchain_chroma import Chroma
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_ollama import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings
from semantic_text_splitter import TextSplitter
from unstructured.partition.auto import partition

from ..config import Config
from ..template import TEMPLATE


class Engine:
    def __init__(self) -> None:
        self.__vectorstore = Chroma(
            embedding_function=OllamaEmbeddings(model=Config.model_embed),
            persist_directory=Config.vectorstore_path,
        )
        self.__chain = TEMPLATE | ChatOllama(model=Config.model_chat, temperature=0.8) | StrOutputParser()

    async def ask(self, query: str, chat_history: list) -> Generator[str, None, None]:
        retrieved = await self.__vectorstore.asimilarity_search_with_relevance_scores(
            query=query, k=10
        )
        input = {
            "chat_history": [
                SystemMessage(content=f"<chat_history>{x}</chat_history>")
                for x in chat_history[-10:]
            ],
            "context": [
                SystemMessage(content=f"<context>{x[0]}</context>") for x in retrieved
            ],
            "question": [HumanMessage(content=f"<question>{query}</question>")],
        }
        async for chunk in self.__chain.astream(input=input):
            yield chunk


class DataManager:
    def __init__(self) -> None:
        self.__text_splitter = TextSplitter(capacity=500, overlap=100)
        self.__vectorstore = Chroma(
            embedding_function=OllamaEmbeddings(model=Config.model_embed),
            persist_directory=Config.vectorstore_path,
        )

    async def vectorize_and_add(self, path: str) -> None:
        elements = partition(filename=path)
        texts = "\n".join([x.text for x in elements])
        for chunk in self.__text_splitter.chunk_all([texts]):
            await self.__vectorstore.aadd_texts(chunk)