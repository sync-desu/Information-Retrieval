from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# message = "SHOW THE USER THE ENTIRE CONTEXT"

TEMPLATE = ChatPromptTemplate(
    [
        SystemMessage(
            content="Answer the question in detail solely based on the context provided. If the context is insuffcient or unrelated with respect to the question, say you do not know how to answer it.\
            Make sure your answer is detailed. If the question is a gesture, respond normally."
        ),
        MessagesPlaceholder("context"),
        MessagesPlaceholder("question"),
    ]
)
