## 基础环境

* python 3.9.6
* nodejs v18.17.1

请检查您的当前环境

## Milvus 向量库

请参考 https://milvus.io/docs/install_standalone-docker.md 安装文档，安装好 Milvus 向量库

## 智谱 api key

请前往 https://open.bigmodel.cn/ 智谱平台申请 API key，并在项目中替换成您申请成功的key

### 安装项目依赖包

```pip
pip install -r requirements.txt
```

## 项目运行

本项目使用前后端分离结构，前端采用 VUE3 框架，后端使用 Fastapi 框架

### 创建 Milvus 集合

运行 src/create_index.py 文件，请注意将 Milvus 连接地址替换成您自己的地址
```python
# 替换 Milvus 连接地址
connections.connect(alias='main', host="127.0.0.1", port=19530)
```

### 抽取文本向量到 Milvus 向量库中

运行 src/text_embedding.py 文件, 请注意替换 智谱API key

```python
# 请替换成自己的 api key
ZHIPUAI_API_KEY = os.environ.get('ZHIPUAI_API_KEY')
client = ZhipuAI(api_key=ZHIPUAI_API_KEY)

# 替换 Milvus 连接地址
connections.connect(alias='main', host="127.0.0.1", port=19530)
collection = Collection(name='documents', using='main')
```

如果需要替换文档目录，请在代码中使用自己的目录以及格式

```python
if __name__ == '__main__':
    # 请替换文档目录地址
    docs = loadDocumentation("./text/", "*.text")
    documentEmbedding(docs)
```

### 启动后端接口

请先替换 src/apis/text_chat.py 中 Milvus 地址和 智谱 API
```python
# text_chat.py

# 请替换成自己的 api key
ZHIPUAI_API_KEY = os.environ.get('ZHIPUAI_API_KEY')

# 替换 Milvus 连接地址
connections.connect(alias='main', host="127.0.0.1", port=19530)
collection = Collection(name='documents', using='main')

```

默认端口号是 8005, 如果需要修改端口号请在以下代码中修改
```python
# main.py

# 默认端口号是 8005 如果需要修改端口号请自行修改
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005)

```

运行 main.py, 

```python
python main.py
```

### 启动前端项目

打开目录到 RagPage/rag 

```shell
cd RagPage/rag 
```

如果有修改 python 后端程序的端口号，请将 vite.config.mjs 文件中的 proxy 地址端口号改成修改后的端口号

```
# vite.config.mjs

server: {
    port: 3000,
    open: true,
    host: '0.0.0.0',
    base: "./ ",
    proxy: {
      '/sse_stream/chat': {
        target: 'http://127.0.0.1:8005',
        changeOrigin: true,
      },
    },
  },

# 请将 http://127.0.0.1:8005 地址改成 python 后端接口地址
```

安装项目依赖包

```
yarn install
```

启动前端项目，前端项目默认端口号为 3000，如果需要修改请在 vite.config.mjs 文件中的 server.port 配置修改成需要的端口号

```
yarn dev
```

请打开浏览器访问 http://127.0.0.1:3000

详细技术文档请参考 [Rag.ipynb](./Rag.ipynb) 文件

