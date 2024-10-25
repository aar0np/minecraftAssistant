import os

from astrapy.constants import Environment
from fastapi import FastAPI, Depends
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_astradb import AstraDBVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel

# define DB vars
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')
TABLE_NAME = "minecraft_vectors"

# LangChain prompt template, LLM, embeddings model, retriever, and chain
minecraft_assistant_template = """
You are an assistant for the game Minecraft, helping players with questions.
Answer the questions with the context provided, but you may use external sources as well.
You must refuse to answer any questions not related to the game Minecraft.

CONTEXT:
{context}

QUESTION: {question}

YOUR ANSWER:"""
minecraft_prompt = ChatPromptTemplate.from_template(minecraft_assistant_template)

llm = ChatOpenAI(model="gpt-4o")
embeddings = OpenAIEmbeddings()

# init LangChain "AstraDB" vectorstore
vectorstore = AstraDBVectorStore(
    embedding=embeddings,
    namespace="default_namespace",
    collection_name=TABLE_NAME,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    environment=Environment.DSE
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | minecraft_prompt
    | llm
    | StrOutputParser()
)

# API code
class AssistantRequest(BaseModel):
	question: str

app = FastAPI()

@app.post('/askAI')
async def ask_assistant(request: AssistantRequest):
	answer = chain.invoke(request.question)

	return { 'answer': answer }
