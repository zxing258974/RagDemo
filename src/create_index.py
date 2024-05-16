from pymilvus import Collection, FieldSchema, DataType, CollectionSchema, connections

# 请替换成您自己的 Milvus 地址
connections.connect(alias='main', host="127.0.0.1", port=19530)


def create_index():
    """
    创建 Milvus 集合，并且为每个 field 创建索引

    请注意 document_ebm 的 dim 参数，词参数代表向量维度，它的大小要和向量后的结果长度一致，否则在写入向量时会报错
    """
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="document_ebm", dtype=DataType.FLOAT_VECTOR, dim=1024),
        FieldSchema(name="document_text", dtype=DataType.VARCHAR, max_length=65535),
    ]
    schema = CollectionSchema(fields=fields)
    # 创建集合
    collection = Collection(name='documents', schema=schema, using='main')
    # 添加 HNSW 索引，索引优势
    # 非常高速的查询
    # 要求召回率尽可能高
    # 大内存资源
    index_params = {
        "index_type": "HNSW",
        "metric_type": "IP",
        "params": {
            "M": 32,
            "efConstruction": 512
        }
    }
    collection.create_index(
        field_name="document_ebm",
        index_params=index_params
    )

    collection.create_index(
        field_name="document_text",
        index_params={
            "index_type": "marisa-trie"
        }
    )
    # 集合创建成功后，将数据加载到内存中
    collection.load()


if __name__ == "__main__":
    create_index()
