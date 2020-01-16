import sys, time
import subprocess
from rc import pmap

sys.path.append('lib')


from cluster import GCloudNode, RpcNode
from utils import chain_query

def print_chain_data(block, file=sys.stdout):
    chunks = []
    for c in block['chunks']:
        chunks.append(f'{c["chunk_hash"]} {c["shard_id"]}')
    print(block['header']['height'], block['header']['hash'], ','.join(chunks), file=file)

subprocess.run('mkdir -p /tmp/100_node/', shell=True)

f = []
for node in range(100):
    f.append(open(f'/tmp/100_node/pytest-node-{node}.txt', 'w'))

def query_node(i):
    node = GCloudNode(f'pytest-node-{i}')
    chain_query(node, lambda b: print_chain_data(b, f[i]), max_blocks=20)

# pmap(query_node, range(100))

node = RpcNode('localhost', 3030)
chain_query(node, print_chain_data, max_blocks=800)