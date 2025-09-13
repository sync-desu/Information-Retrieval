from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

TEMPLATE = ChatPromptTemplate(
    [
        SystemMessage(
            content="Answer the user provided QUESTION solely based on the CONTEXT provided. If the CONTEXT is INSUFFICIENT or UNRELATED to the QUESTION, say you dont know how to answer it. However, if the QUESTION is with regards to YOU, or to the USER, then do answer it gracefully. Ensure anything out of context is not answered.\
            You are also given with some CHAT HISTORY, which corresponds to the CHAT HISTORY between YOU and the USER, and you also may refer to this to answer. DO NOT MIX UP CHAT HISTORY WITH CONTEXT."
        ),
        MessagesPlaceholder("chat_history"),
        MessagesPlaceholder("context"),
        MessagesPlaceholder("question"),
    ]
)
