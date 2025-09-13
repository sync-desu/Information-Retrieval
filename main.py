from typing import cast, Generator

import chainlit as cl
from langchain_core.messages import AIMessage, HumanMessage

from src.engine import Engine, DataManager


@cl.cache
def get_engine():
    return Engine()


@cl.cache
def get_datamanager():
    return DataManager()


@cl.on_chat_start
async def on_chat_start() -> None:
    cl.user_session.set("chat_history", [])
    cl.user_session.set("engine", get_engine())
    cl.user_session.set("datamanager", get_datamanager())
    await cl.Message(content="Please feel free to ask anything about the document.").send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    engine = cast(Engine, cl.user_session.get("engine"))
    chat_history = cast(list, cl.user_session.get("chat_history"))
    msg = cl.Message(content="")
    async for chunk in engine.ask(query=message.content, chat_history=chat_history):
        await msg.stream_token(chunk)
    chat_history.append({"role": "user", "content": message.content})
    chat_history.append({"role": "assistant", "content": msg.content})
