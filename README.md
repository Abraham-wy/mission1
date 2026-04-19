总所周知，联网搜索能力已经是大模型重要的能力。检索数据的准确度将决定了大模型回答能力的正确性。此外，在一些专业领域大模型中，RAG技术得到广泛运用已解决其幻觉问题。

在RAG中，使用embedding对文档句子进行编码，使其转化高纬度向量是基础工作，现在有一个法律问答数据集，请你这个数据集里的数据通过编码，送入Elasticsearch向量检索中。简而言之，即使用elasticsearch构建一个向量数据库。

**技术要求**：

1.  使用Elasticsearch建立向量索引

2.  使用Bert等embedding模型对数据编码，并存入ES中

**提交要求**：

1.  索引的属性截图，证明其是向量索引。

    ![](media/image1.png){width="5.997222222222222in"
    height="3.079861111111111in"}

2.  ES向量查询结果，证明其向量检索有效。

    ![](media/image2.png){width="5.997222222222222in"
    height="3.0756944444444443in"}

**建议：**

可参考RAGflow项目的docker，省去配置环境的时间

https://github.com/infiniflow/ragflow
