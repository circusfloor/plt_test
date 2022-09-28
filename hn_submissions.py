import requests

from operator import  itemgetter

# 执行API调用并存储响应
url = r'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print('status code:', r.status_code)

# 处理有关每篇文章的信息
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # 对于每一篇文章，都执行一个API调用
    url = ('https://hacker-news.firebaseio.com/v0/item/' + str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    respose_dict = submission_r.json()

    submission_dict = {
        'title': respose_dict['title'],
        'link': 'https://hacker-news.firebaseio.com/v0/item?id=' + str(submission_id),
        'comments': respose_dict.get('descendants', 0)
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

for submission_dict in submission_dicts:
    print('\ntitle:', submission_dict['title'])
    print('discussion link:', submission_dict['link'])
    print('comments:', submission_dict['comments'])
