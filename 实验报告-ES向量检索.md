# 基于 Elasticsearch 的向量数据库构建实验报告（RAG 数据入库与检索）

**姓名/学号：**（填写）\
**课程/作业：**（填写）\
**日期：**2026-04-19\
**仓库：**Abraham-wy/mission1\
**数据文件：**documents.json（字段：id、HTML_txt）

------------------------------------------------------------------------

## 1. 实验目标

1.  使用 Elasticsearch 建立向量索引（向量字段类型为 dense_vector）。
2.  使用 BERT/Embedding 模型对法律文书数据进行编码，并将向量写入
    Elasticsearch。
3.  通过向量检索（kNN）返回相似文档，证明向量检索有效。
4.  提交两项证据：
    - 索引属性截图：证明是向量索引（dense_vector）。
    - 向量查询结果截图：证明检索有效。

------------------------------------------------------------------------

## 2. 实验环境

- 操作系统：Windows（填写版本，如 Windows 10/11）
- Python：3.10（实际以 `python --version` 为准）
- Elasticsearch：8.12.2（Docker 启动，地址 http://localhost:9200）
- Embedding 模型：`shibing624/text2vec-base-chinese`
- 向量维度：768
- 相似度度量：cosine（余弦相似度）

------------------------------------------------------------------------

## 3. 数据说明与预处理

### 3.1 数据结构

`documents.json` 为 JSON 数组，每条数据包含： - `id`：文档唯一标识 -
`HTML_txt`：法律文书 HTML 内容

### 3.2 为什么要做 HTML → 纯文本

Embedding 模型主要针对自然语言文本。HTML 标签会引入噪声，因此先用 HTML
解析工具提取正文文本，再进行编码。

------------------------------------------------------------------------

## 4. Elasticsearch 向量索引创建

### 4.1 索引名称

- `law_docs`

### 4.2 字段设计（Mapping）

- `id`：keyword
- `html`：text（保留原 HTML，便于追溯）
- `text`：text（HTML 清洗后的纯文本）
- `embedding`：dense_vector（dims=768，index=true，similarity=cosine）

### 4.3 向量索引证明（截图 1）

通过接口查看 mapping：

    curl.exe "http://localhost:9200/law_docs/_mapping?pretty"

截图中需显示（关键字段）：

    "embedding": {
      "type": "dense_vector",
      "dims": 768,
      "index": true,
      "similarity": "cosine"
    }

![](media/image1.png){width="5.997222222222222in"
height="3.079861111111111in"}

## 5. 文档向量化与写入 Elasticsearch

### 5.1 使用的 Embedding 模型

- `shibing624/text2vec-base-chinese`

### 5.2 入库流程说明

对每条文档执行： 1. 读取 `HTML_txt` 2. HTML 清洗得到 `text` 3. 使用
embedding 模型将 `text` 编码为 768 维向量 4. 写入 Elasticsearch 索引
`law_docs` 的 `embedding` 字段

### 5.3 写入验证

可通过计数接口确认写入数量（示例）：

    curl.exe "http://localhost:9200/law_docs/_count?pretty"

------------------------------------------------------------------------

## 6. 向量检索验证（kNN）

### 6.1 检索原理说明

- 将查询文本也编码成向量 `query_vector`
- 使用 Elasticsearch kNN 在 `embedding` 字段上做向量相似检索
- 返回 top-k 相似文档（按 cosine 相似度）

### 6.2 查询示例

查询内容：

- `合同纠纷`` ``违约责任`` ``如何承担`

程序输出示例包含： - `Query = ...` - Top 5 文档的
`score`、`id`、文本预览 `preview`

![](media/image2.png){width="5.997222222222222in"
height="3.0756944444444443in"}

## 7. 实验结论

本实验成功完成以下内容： 1. 在 Elasticsearch 中创建包含 `dense_vector`
字段的向量索引 `law_docs`，并启用向量索引（index=true）。 2. 使用中文
BERT embedding 模型将法律文书文本编码为 768 维向量并写入 Elasticsearch。
3. 使用 kNN
向量检索对输入查询进行相似度搜索，返回相关法律文书结果，证明向量检索有效。

------------------------------------------------------------------------

## 8. 附录（可选）

- ES 地址：`http://localhost:9200`
- 索引名：`law_docs`
- 向量维度：768
- 相似度：cosine
