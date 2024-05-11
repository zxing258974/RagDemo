from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import json
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.callbacks.manager import CallbackManager
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_core.messages import SystemMessage
from langchain.prompts import HumanMessagePromptTemplate

import os
import asyncio
from pymilvus import Collection, connections
from src.text_embedding import getEmbedding

router = APIRouter()

# 请替换成自己的 key
ZHIPUAI_API_KEY = os.environ.get('ZHIPUAI_API_KEY')

# 请替换成您自己的 Milvus 地址
connections.connect(alias='main', host="127.0.0.1", port=19530)
collection = Collection(name='documents', using='main')


@router.get("/sse_stream/chat")
async def userSseChat(question: str):
    async def sse_chat_generator():
        async for token in sse_chat_bot(question=question):
            yield token

    return EventSourceResponse(sse_chat_generator(), media_type="text/event-stream")


async def sse_chat_bot(question: str):
    """ 根据问题和查询到的文档内容调用AI大语言模型回答提出的问题 """
    # 根据问题查询最相似的文档
    documents = getDocuments(question)
    print("查询到的文档")
    print(f"\033[92m{documents}\033[0m")
    callback = AsyncIteratorCallbackHandler()
    # 使用智谱大语言模型，这里我们使用流式输出
    streaming_chat = ChatZhipuAI(
        model="glm-3-turbo",
        api_key=ZHIPUAI_API_KEY,
        temperature=0.01,
        streaming=True,
        callback_manager=CallbackManager([callback]),
    )
    # 定义用户的提示词
    general_user_template = general_user_template = """
请基于以下内容:
\"\"\"
{context}
\"\"\"
来回答用户提出的问题，请用中文回答。

问题: {question}"""

    human_message = HumanMessagePromptTemplate.from_template(general_user_template, input_variables=["question", "context"])
    # 定义系统提示词，规定大语言模型只能使用文档内容来回答用户提出的问题，不要使用自身的知识库
    messages = [
        SystemMessage(content="请根据以下内容回答提出的问题，不要使用自身知识回答问题，回答的越详细越好"),
        human_message.format(question=question, context='/n'.join(documents)),
    ]

    agenerate = streaming_chat.agenerate([messages])
    finalAnswer = asyncio.create_task(agenerate)
    # 流式返回AI得结果
    async for token in callback.aiter():
        yield json.dumps({
            'output': token,
            'end': False
        }, ensure_ascii=False)

    result = await finalAnswer

    yield json.dumps({
        'output': result.generations[0][0].text,
        'end': True
    }, ensure_ascii=False)


def getDocuments(question: str):
    """ 根据问题在向量库中检索最相似的文档，
    首先将问题转换成向量，再在向量库中查询最相似的文档内容，并将文档返回
    """
    # 先将问题转成向量
    query_vector = getEmbedding(question)
    # 在向量库中查询最相似的 topk 1 结果
    search_params = {"metric_type": "IP", "params": {"nprobe": 16}, "offset": 0}
    results = collection.search(data=[query_vector], anns_field='document_ebm', param=search_params, limit=1, output_fields=['document_text'])
    documents = []
    for result in results:
        for r in result:
            document_text = str(r.entity.get('document_text'))
            documents.append(document_text)
    # 返回文档内容
    return documents
