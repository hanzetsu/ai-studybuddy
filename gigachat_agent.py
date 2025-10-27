from langchain.llms import GigaChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = GigaChat(
    client_id=os.getenv("GIGACHAT_CLIENT_ID"),
    client_secret=os.getenv("GIGACHAT_CLIENT_SECRET"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    temperature=0.2,           # Минимальная креативность
    max_tokens=200,            # Ограничение на длину ответа
)

# Основной шаблон для ответов на вопросы студентов
qa_prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "Ты — умный и доброжелательный помощник студента МИФИ. "
        "Отвечай точно, сжато и понятно. Объясняй с позиции преподавателя.\n\n"
        "Вопрос: {question}\n\nОтвет:"
    )
)

chain = LLMChain(llm=llm, prompt=qa_prompt)

def answer_question(question: str) -> str:
    return chain.run(question)

# Объяснение простыми словами
simple_prompt = PromptTemplate(
    input_variables=["answer"],
    template=(
        "Объясни это простыми словами, как будто рассказываешь первокурснику:\n{answer}"
    )
)

simple_chain = LLMChain(llm=llm, prompt=simple_prompt)

def explain_simple(answer: str) -> str:
    return simple_chain.run(answer)
