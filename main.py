from whoosh.qparser import MultifieldParser
from whoosh.index import open_dir
from whoosh.query import And
from whoosh import qparser
import string

def search_keywords(keywords, index_dir):
    ix = open_dir(index_dir)
    # 创建一个解析器，可以解析content和title字段
    parser = MultifieldParser(["content", "title"], ix.schema, group=qparser.OrGroup.factory(0.9))  # 使用OrGroup，并设置奖励因子

    # 添加模糊搜索插件
    parser.add_plugin(qparser.FuzzyTermPlugin())

    # 构造 And 组合子查询，确保搜索结果必须包含所有关键字
    query = And([parser.parse(keyword) for keyword in keywords])

    # 存储搜索结果的列表
    results = []
    with ix.searcher() as searcher:
        # 设置按时间戳字段降序排序
        hits = searcher.search(query, sortedby="time", reverse=True)
        for hit in hits:
            # 将时间字段转换为时间戳
            time_stamp = hit["time"]
            results.append({"id": hit["id"], "title": hit["title"], "time": time_stamp})

    return results  # 返回字典列表

if __name__ == "__main__":
    query = input("Enter search terms: ")

    # 去除标点符号
    query = ''.join(char for char in query if char not in string.punctuation)

    # 将查询字符串拆分为单个字符的列表
    characters = list(query)

    # 构造查询字符串，在每个字符之间插入 "AND" 操作符
    query_with_and = "AND".join(characters)

    keywords = query_with_and.split()

    print("Search in content and title:")
    results = search_keywords(keywords, 'indexdir')  # 使用原始的关键字列表
    for result in results:
        print("ID:", result['id'], "Title:", result['title'], "Time (Timestamp):", result['time'])
