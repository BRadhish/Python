from elasticsearch import Elasticsearch
from elasticsearch.client.ingest import IngestClient
import argparse
import json
from ssl import create_default_context

context = create_default_context(cafile="PEMfilelocation")
es = Elasticsearch('APIlinkgoeshere',
    http_auth=('', ''),
    scheme="https",
    port=9200,
    ssl_context=context,
)

def load_watch():
    with open('alertbody2.json','r') as watch_file:
            watch=json.loads(watch_file.read())
            es.watcher.put_watch(id = 'Error-watch',body=watch)
            response=es.watcher.execute_watch(id='Error-watch')
            print("Watcher created successfully")

def watch_stats():
    statis = es.watcher.stats()
    for s in statis['stats']:
        print("Watch count : ",s['watch_count'])
        print("Node ID: ", s['node_id'])
        print("Queue size: ", s['execution_thread_pool']['queue_size'])
        print("Max size: ",s['execution_thread_pool']['max_size'])
        #print(s['manually_stopped'])
        print("/////////////////////////////")
#functioncall
load_watch()
watch_stats()
