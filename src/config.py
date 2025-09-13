from dataclasses import dataclass


class _Config:
    model_chat: str = r"llama3.1:8b-instruct-q4_K_M"
    model_embed: str = r"nomic-embed-text:137m-v1.5-fp16"
    vectorstore_path: str = r"src\vectorstore"


Config = _Config()
