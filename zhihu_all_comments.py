import requests
import pymongo
import time


# 第一页种子
def get_comment_page(page):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36'
    }
    # 问题：如何看待温州乐清 20 岁女生乘坐滴滴顺风车遇害 ？是否反应出客服系统存在问题？
    url = 'https://www.zhihu.com/api/v4/answers/477622227/comments?include=data%5B*%5D.author%2Ccollapsed' \
          '%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author' \
          '%2Calgorithm_right&order=normal&limit=20&offset='+ str(page*20)+'&status=open'
    response = requests.get(url, headers=header)
    return response.json()


# 解析函数
def parse_comments(html):
    paging = html['paging']
    is_end = paging['is_end']
    # is_end:True,False
    items = html['data']
    for item in items:
        comment = item['content']
        vote_count = item['vote_count']
        name = item['author']['member']['name']
        print(name, ':', comment, end='||')
        print('赞同数:', vote_count)
        print('-' * 60)
        info = {
            'name': name,
            'comment': comment,
            'vote_count': vote_count
        }
        save_to_mongo(info)
        print('-' * 100)

    return is_end


# 连接到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'zhihu_comments'
MONGO_COLLECTION = 'comments_1'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]


def save_to_mongo(data):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(data):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


if __name__ == '__main__':
    i = 0
    print('正在爬取问题：')
    print('"如何看待温州乐清 20 岁女生乘坐滴滴顺风车遇害 ？是否反应出客服系统存在问题？"')
    print('的评论...')
    print('='*100)
    while (1):
        i = i + 1
        html = get_comment_page(i-1)
        end = parse_comments(html)
        time.sleep(2)
        if end == True:
            break
