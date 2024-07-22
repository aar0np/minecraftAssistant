import os
#import cassio

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from fastapi import FastAPI, Depends
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import Cassandra
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel

# define DB vars
CASSANDRA_ENDPOINT = os.environ.get("CASSANDRA_ENDPOINT")
CASSANDRA_USERNAME = os.environ.get("CASSANDRA_USERNAME")
CASSANDRA_PASSWORD = os.environ.get('CASSANDRA_PASSWORD')
CASSANDRA_KEYSPACE = "default_keyspace"
TABLE_NAME = "minecraft_vectors_cass"

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

# Cassandra connection
auth_provider = PlainTextAuthProvider(username=CASSANDRA_USERNAME, password=CASSANDRA_PASSWORD)
cluster = Cluster([CASSANDRA_ENDPOINT],auth_provider=auth_provider)
session = cluster.connect()

# wires-up LangChain and Cassandra "behind the scenes"
#cassio.init(session=session, keyspace=CASSANDRA_KEYSPACE)

# init LangChain "Cassandra" vectorstore
vectorstore = Cassandra(
    embedding=embeddings,
    table_name=TABLE_NAME,
    session=session,
    keyspace=CASSANDRA_KEYSPACE
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

