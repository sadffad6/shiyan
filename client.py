import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from datetime import datetime
from jieba.analyse import ChineseAnalyzer  # 导入中文分词器

def create_search_index(data, index_dir):
    # 定义模式
    schema = Schema(id=ID(stored=True, unique=True), title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                    content=TEXT(stored=True, analyzer=ChineseAnalyzer()), time=NUMERIC(stored=True))  # 添加了时间字段的定义

    # 如果索引目录不存在，则创建
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    # 创建索引
    ix = create_in(index_dir, schema)

    writer = ix.writer()

    for i, item in enumerate(data, start=1):
        writer.add_document(id=str(i), title=item['title'], content=item['content'], time=item['time'])  # 修改为使用时间字段

    writer.commit()
    print(f"Index created in {index_dir}")

if __name__ == '__main__':
    data = [
        {"title": "你好啊！小朋友", "content": "我是一个人.", "time": datetime(2024, 5, 1).timestamp()},
        {"title": "Document 2", "content": "我是两个人", "time": datetime(2024, 5, 2).timestamp()},
        {"title": "Document 3", "content": "我是三个人", "time": datetime(2024, 5, 3).timestamp()}
    ]

    create_search_index(data, "indexdir")
