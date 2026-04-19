from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

ES_URL = "http://localhost:9200"
INDEX = "law_docs"

# 连接 ES
es = Elasticsearch(ES_URL)

# 加载同一个 embedding 模型（必须一致，保证向量空间一致）
model = SentenceTransformer("shibing624/text2vec-base-chinese")

# 你要查询的问题/关键词（你可以换成任何中文法律问题）
query = "合同纠纷 违约责任 如何承担"

# 把查询文本变成向量
qvec = model.encode(query, normalize_embeddings=True).tolist()

# kNN 检索：找最相似的 5 条
resp = es.search(
    index=INDEX,
    knn={
        "field": "embedding",
        "query_vector": qvec,
        "k": 5,
        "num_candidates": 50
    },
    source=["id", "text"]
)

print("Query =", query)
for i, hit in enumerate(resp["hits"]["hits"], 1):
    src = hit["_source"]
    preview = src["text"][:120].replace("\n", " ")
    print(f"{i}. score={hit['_score']:.4f} id={src['id']} preview={preview}...")