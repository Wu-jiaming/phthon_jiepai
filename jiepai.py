import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import  Pool
import json
from pymongo import MongoClient

#获取页面的response
def get_page(offset):
    params={
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'from':'search_tab'

    }
    url = 'https://www.toutiao.com/search_content/?'+urlencode(params)

    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.json()

    except requests.ConnectionError:
        print('ConnectionError:')
        return  None

#从response获取照片url，并用yield迭代
def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_detail')
            for image in images:
                yield{
                    'image':image.get('url'),
                    'title':title
                }
#保存照片
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))

    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('Already DownLoaded',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

#写入文件
def write_file(item):
    with open('jiepai.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')

#保存到mongodb
def save_mongodb(item):
    client = MongoClient()
    db = client['jiepai']
    collection = db['jiepai']
    if collection.insert(item):
        print('Save to mongodb')
    else:
        print("can't save to mongodb")



def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        write_file(item)
        save_image(item)
        save_mongodb(item)

GROUP_START = 1
GROUP_END = 1

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START,GROUP_END+1)])
    pool.map(main,groups)
    # 调用join之前，先调用close函数，否则会出错。
    # 执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    pool.close()
    pool.join()
