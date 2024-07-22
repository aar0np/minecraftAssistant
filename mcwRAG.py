import os

#from astrapy.constants import Environment
#from astrapy import DataAPIClient
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import cassio
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
#from langchain_astradb import AstraDBVectorStore
from langchain_community.vectorstores import Cassandra
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# define DB vars
#ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")
#ASTRA_DB_APPLICATION_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')
CASSANDRA_ENDPOINT = os.environ.get("CASSANDRA_ENDPOINT")
CASSANDRA_USERNAME = os.environ.get("CASSANDRA_USERNAME")
CASSANDRA_PASSWORD = os.environ.get('CASSANDRA_PASSWORD')
CASSANDRA_KEYSPACE = "default_keyspace"
#TABLE_NAME = "minecraft_vectors"
TABLE_NAME = "minecraft_vectors_cass"

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
cassio.init(session=session, keyspace=CASSANDRA_KEYSPACE)

vectorstore = Cassandra(
    embedding=embeddings,
    table_name=TABLE_NAME
)

## Astra DB connection
#client = DataAPIClient(token=ASTRA_DB_APPLICATION_TOKEN, environment=Environment.HCD)
#db = client.get_database(api_endpoint=ASTRA_DB_API_ENDPOINT,namespace="default_keyspace")

#vectorstore = AstraDBVectorStore(
#    embedding=embeddings,
#    collection_name=TABLE_NAME,
#    astra_db_client=db,
#)

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

