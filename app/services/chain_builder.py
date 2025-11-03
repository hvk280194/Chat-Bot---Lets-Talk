from typing import List, Dict
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM = "You are a concise, helpful assistant. Keep answers under 200 words unless asked."

def build_prompt(input_text: str, history: List[Dict[str, str]]):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    return prompt.format_messages(history=history, input=input_text)
