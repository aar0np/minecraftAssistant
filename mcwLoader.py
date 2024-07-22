import os
import json

#from astrapy.constants import Environment
#from astrapy import DataAPIClient
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import cassio
#from langchain_astradb import AstraDBVectorStore
from langchain_community.vectorstores import Cassandra
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# DB connection
#ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
#ASTRA_DB_API_ENDPOINT= os.environ.get("ASTRA_DB_API_ENDPOINT")
CASSANDRA_ENDPOINT = os.environ.get("CASSANDRA_ENDPOINT")
CASSANDRA_USERNAME = os.environ.get("CASSANDRA_USERNAME")
CASSANDRA_PASSWORD = os.environ.get('CASSANDRA_PASSWORD')
CASSANDRA_KEYSPACE = "default_keyspace"
TABLE_NAME = "minecraft_vectors_cass"

auth_provider = PlainTextAuthProvider(username=CASSANDRA_USERNAME, password=CASSANDRA_PASSWORD)
cluster = Cluster([CASSANDRA_ENDPOINT],auth_provider=auth_provider)
session = cluster.connect()
cassio.init(session=session, keyspace=CASSANDRA_KEYSPACE)

#client = DataAPIClient(token=ASTRA_DB_APPLICATION_TOKEN, environment=Environment.HCD)
#db = client.get_database(ASTRA_DB_API_ENDPOINT,namespace="default_keyspace")

# using OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)

## create "collection" (vector-enabled table)
#collection = db.create_collection(TABLE_NAME, dimension=1536, metric="cosine")

vectorstore = Cassandra(
    embedding=embeddings,
    table_name=TABLE_NAME
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 10,
    length_function = len,
    is_separator_regex = False,
)

linecounter = 0

# iterate through all of the Minecraft text files
for counter in range(1,6):
	textfile = str(counter) + ".txt"

	docs = []
	with open(textfile) as ft:
		doc = ft.read()
		texts = text_splitter.split_text(doc)

		for index in range(0,len(texts)):
			text = str(texts[index]).strip().replace("\n"," ").replace("\"","\\\"")
			emb = embeddings.embed_query(text)

			#strJson = '{"text":"' + text + '","$vector":' + str(emb) + '}'
			#document = json.loads(strJson)
			document = Document(page_content=text);

			#collection.insert_one(doc)
			docs.append(document)
			linecounter = linecounter + 1

	vectorstore.add_documents(docs)
	print(f"{textfile} successfully processed.")
