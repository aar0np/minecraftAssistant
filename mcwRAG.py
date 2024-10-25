import os

from astrapy.constants import Environment
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_astradb import AstraDBVectorStore
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# define DB vars
ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')
CASSANDRA_KEYSPACE = "default_namespace"
TABLE_NAME = "minecraft_vectors"

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

vectorstore = AstraDBVectorStore(
    embedding=embeddings,
    namespace="default_namespace",
    collection_name=TABLE_NAME,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    token=ASTRA_DB_APPLICATION_TOKEN,
    environment=Environment.DSE\
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | minecraft_prompt
    | llm
    | StrOutputParser()
)

userInput = "What is the recipe for an iron helmet?"

print(f"Question? {userInput}")

while userInput != "exit":
    print(chain.invoke(userInput))
    print("\n")
    userInput = input("Next question? ")

print("Exiting...")

