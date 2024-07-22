# Minecraft Assistant
A console and API-based AI assistant built in Python using LangChain and OpenAI; designed to run on DataStax Hyper-Converged Database (HCD).

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
 	- fastapi 0.111.1
 	- langchain 0.2.9
 	- langchain-openai 0.1.17
 	- langchain-community 0.2.7
 - Environment variables:
 	- CASSANDRA_ENDPOINT
 	- CASSANDRA_USERNAME
 	- CASSANDRA_PASSWORD
 	- CASSANDRA_KEYSPACE
 	- OPENAI_API_KEY

## Data Loading

### Database schema

Created automatically by the LangChain-Community `Cassandra` library.

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

After running the loader, you should see the following table in the `default_keyspace`:

```
CREATE TABLE default_keyspace.minecraft_vectors_cass (
    row_id text PRIMARY KEY,
    attributes_blob text,
    body_blob text,
    vector vector<float, 1536>,
    metadata_s map<text, text>
) WITH additional_write_policy = '99p'
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND cdc = false
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.UnifiedCompactionStrategy'}
    AND compression = {'chunk_length_in_kb': '16', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND memtable = {}
    AND crc_check_chance = 1.0
    AND default_time_to_live = 0
    AND extensions = {}
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair = 'BLOCKING'
    AND speculative_retry = '99p';

CREATE CUSTOM INDEX eidx_metadata_s_minecraft_vectors_cass ON default_keyspace.minecraft_vectors_cass (entries(metadata_s)) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex';

CREATE CUSTOM INDEX idx_vector_minecraft_vectors_cass ON default_keyspace.minecraft_vectors_cass (vector) USING 'org.apache.cassandra.index.sai.StorageAttachedIndex';
```

## Running the console-based AI Assistant

```
python mcwRAG.py

Question? What is the recipe for an iron helmet?
In Minecraft, the recipe for crafting an iron helmet requires 5 iron ingots. To craft it, you need to place the iron ingots in the following pattern on a crafting table (3x3 grid):

1. Place 3 iron ingots in the top row.
2. Place 1 iron ingot in the left slot of the middle row.
3. Place 1 iron ingot in the right slot of the middle row.

Here's a visual representation of the crafting grid:

[Iron Ingot] [Iron Ingot] [Iron Ingot]
[Iron Ingot] [Empty]     [Iron Ingot]
[Empty]      [Empty]     [Empty]

Once you have arranged the iron ingots in this pattern on the crafting table, you can then drag the iron helmet to your inventory.
```

## Running the API-based AI Assistant

```
uvicorn mcwRAGAPI:app
```

### Testing the API

```
curl -s -XPOST http://127.0.0.1:8000/askAI \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{"question":"What is the recipe for a gold sword?"}'

{"answer":"To craft a gold sword in Minecraft, you will need the following ingredients:\n\n- 2 Gold Ingots\n- 1 Stick\n\nHere's the crafting recipe:\n\n1. Open your Crafting Table (3x3 crafting grid).\n2. Place the 2 Gold Ingots in the middle column:\n   - 1st Gold Ingot in the top-middle slot.\n   - 2nd Gold Ingot in the middle slot.\n3. Place the Stick in the bottom-middle slot.\n\nThe gold sword will appear in the result box, and you can then drag it into your inventory."}
```
