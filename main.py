from typing import Generator, cast

import chainlit as cl
from langchain_core.messages import AIMessage, HumanMessage

from src.engine import DataManager, Engine


@cl.cache
def get_engine():
    return Engine()


@cl.cache
def get_datamanager():
    return DataManager()


@cl.on_chat_start
async def on_chat_start() -> None:
    cl.user_session.set("engine", get_engine())
    cl.user_session.set("datamanager", get_datamanager())
    await cl.Message(
        content="Please feel free to ask anything about the document."
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    engine = cast(Engine, cl.user_session.get("engine"))
    msg = cl.Message(content="")
    response = await engine.ask(query=message.content)
    async for chunk in response[0]:
        await msg.stream_token(chunk)
    if response[1]:
        await msg.stream_token("\n\n**Citations:**\n")
    for document in response[1][:3]:
        streamable = (
            "─────────────────────────────────────────────────────────────\n"
            + document[0].page_content[:150].replace("\n", " ")
            + "..."
            + f"\n**Source**\n    └── **{document[0].metadata['filename']}** (page {document[0].metadata['page']})\n\n"
        )
        await msg.stream_token(streamable)
