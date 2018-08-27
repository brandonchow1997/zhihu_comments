
# 问题：如何看待温州乐清 20 岁女生乘坐滴滴顺风车遇害 ？是否反应出客服系统存在问题？
import requests
import pymongo
import time


##########################################################
# 获取所有回答
def get_answer(offset):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36'
    }
    answer_url = 'https://www.zhihu.com/api/v4/questions/291804959/answers?include=data%5B%2A%5D.is_normal' \
                 '%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail' \
                 '%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment' \
                 '%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission' \
                 '%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship' \
                 '.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D' \
                 '.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit' \
                 '=5&offset='+str(offset * 5)+'&sort_by=default '
    response = requests.get(answer_url, headers=header)
    return response.json()


# 解析回答的id
def parse_answer_id(html):
    paging = html['paging']
    is_end = paging['is_end']
    items = html['data']
    for item in items:
        id = item['id']
        author = item['author']['name']
        print('回答者:', author, end='||')
        print('回答id:', id)
        time.sleep(2)
        comments(id)
    return is_end
##########################################################


##########################################################
def get_comment_page(id, page):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.12 Safari/537.36'
    }

    url = 'https://www.zhihu.com/api/v4/answers/' + str(id) + '/comments?include=data%5B*%5D.author%2Ccollapsed' \
          '%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author' \
          '%2Calgorithm_right&order=normal&limit=20&offset=' + str(page*20)+'&status=open'
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
        print(name, '\n', comment, end='||')
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
##########################################################

# 连接到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'zhihu_comments'
MONGO_COLLECTION = 'comments_1'
client = pymongo.MongoClient(MONGO_URL, port=27017)
db = client[MONGO_DB]


# 存储到数据库
def save_to_mongo(data):
    # 保存到MongoDB中
    try:
        if db[MONGO_COLLECTION].insert(data):
            print('存储到 MongoDB 成功')
    except Exception:
        print('存储到 MongoDB 失败')


def answer():
    i = 0
    while (1):
        i = i + 1
        data = get_answer(i-1)
        end = parse_answer_id(data)
        time.sleep(2)
        if end == True:
            break


##########################################################
def comments(id):
    j = 0
    while (1):
        j = j + 1
        html = get_comment_page(id, j-1)
        end = parse_comments(html)
        time.sleep(2)
        if end == True:
            break


##########################################################
if __name__ == '__main__':
    print('正在爬取：')
    print('"如何看待温州乐清 20 岁女生乘坐滴滴顺风车遇害 ？是否反应出客服系统存在问题？"')
    print('的评论...')
    print('='*100)
    answer()


