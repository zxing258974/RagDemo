from langchain_community.document_loaders import DirectoryLoader
from zhipuai import ZhipuAI
import os
from pymilvus import Collection, connections

# 请替换成自己的 key
ZHIPUAI_API_KEY = os.environ.get('ZHIPUAI_API_KEY')
client = ZhipuAI(api_key=ZHIPUAI_API_KEY)

# 请替换成您自己的 Milvus 地址
connections.connect(alias='main', host="127.0.0.1", port=19530)
collection = Collection(name='documents', using='main')


def loadDocumentation(path: str, glob: str = "*.text"):
    """利用 langchain 框架的文本阅读器读取目录下指定文件"""
    loader = DirectoryLoader(path=path, glob=glob)
    return loader.load()


def documentEmbedding(docs):
    """ 将文本数据转换成向量，并存储到向量库中 """
    document_ebm = []
    document_text = []
    for doc in docs:
        embedding = getEmbedding(doc.page_content)
        document_ebm.append(embedding)
        document_text.append(doc.page_content)

    documents = [document_ebm, document_text]
    # 批量写入数据
    res = collection.insert(data=documents)
    collection.flush()
    # 打印结果
    print(f"插入行数 -> {res.insert_count}")


def getEmbedding(text):
    """ 调用智谱 embedding-2 模型，将文本转换成向量"""
    response = client.embeddings.create(
        model="embedding-2",
        input=text,
    )
    return response.data[0].embedding


if __name__ == '__main__':
    # 读取文档
    docs = loadDocumentation("./text/", "*.text")
    documentEmbedding(docs)
