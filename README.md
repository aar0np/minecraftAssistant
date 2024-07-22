# Minecraft Assistant
An AI assistant built in Python using LangChain and OpenAI; designed to run on DataStax Hyper-Converged Database (HCD).

## Requirements
 - Built on Python 3.12
 - One of the following vector-enabled, Cassandra-compatible databases:
 	- Apache Cassandra® 5.0
 	- DSE 6.9
 	- HCD 1.0
 	- Astra DB (_connection code is commented-out, but present_)
 - Install the following libraries w/ Pip:
 	- cassandra-driver 3.29.1
 	- cassio 0.1.8
 	- langchain 0.2.9
 	- langchain-openai 0.1.17
 	- langchain-community 0.2.7
 - Environment variables:
 	- CASSANDRA_ENDPOINT
 	- CASSANDRA_USERNAME
 	- CASSANDRA_PASSWORD
 	- CASSANDRA_KEYSPACE

## Data Loading

### Web scraping
_Text file are included in the repo, because this step is a bit messy._

```
python mcwScraper.py
```

### Process HTML into TXT files
_Text file are included in the repo, because this step is a bit messy._

```
python mcwFileProcessor.py
```

### Load TXT files

```
python mcwLoader.py
```

## Running the AI Assistant

```
python mcwRAG.py

Question? What is the recipe for an iron helmet?
In Minecraft, the recipe for crafting an iron helmet requires 5 iron ingots. To craft it, you need to place the iron ingots in the following pattern on a crafting table (3x3 grid):

1. Place 3 iron ingots in the top row.
2. Place 1 iron ingot in the left slot of the middle row.
3. Place 1 iron ingot in the right slot of the middle row.

Here's a visual representation of the crafting grid:

```
[Iron Ingot] [Iron Ingot] [Iron Ingot]
[Iron Ingot] [Empty]     [Iron Ingot]
[Empty]      [Empty]     [Empty]
```

Once you have arranged the iron ingots in this pattern on the crafting table, you can then drag the iron helmet to your inventory.
```