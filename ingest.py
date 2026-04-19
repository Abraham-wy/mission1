import json
from tqdm import tqdm
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

ES_URL = "http://localhost:9200"
INDEX = "law_docs"
DATA_PATH = "documents.json"

def html_to_text(html: str) -> str:
    # 解释：BeautifulSoup 用来解析 HTML；get_text() 提取纯文本
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(separator="\n")

    # 解释：做一点清洗，去掉空行，让文本更干净
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)

# 解释：连接 Elasticsearch 服务（localhost:9200）
es = Elasticsearch(ES_URL)

# 解释：加载 embedding 模型（把文本变成向量）
model = SentenceTransformer("shibing624/text2vec-base-chinese")

# 解释：dims 是向量长度，必须和你索引 mapping 的 dims 一致
dim = model.get_sentence_embedding_dimension()
print("embedding dim =", dim)
print("Make sure it matches mapping dims (currently 768).")

# 解释：读取你的数据集（一个 JSON 数组，每条有 id 和 HTML_txt）
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 解释：逐条处理并写入 ES
for item in tqdm(data):
    doc_id = item["id"]
    html = item.get("HTML_txt", "")
    text = html_to_text(html)

    # 解释：把 text 编码成向量；normalize_embeddings=True 便于用 cosine 相似度
    vec = model.encode(text, normalize_embeddings=True).tolist()

    # 解释：写入 ES 的文档结构
    doc = {
        "id": doc_id,
        "html": html,
        "text": text,
        "embedding": vec
    }

    es.index(index=INDEX, id=doc_id, document=doc)

print("done")