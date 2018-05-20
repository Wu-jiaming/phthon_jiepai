import json
import requests
from requests.exceptions import RequestException
import re
import time
import sys
                         

# 获取url的html
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }

        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#根据正则表达式分组 并且获取有效数据
def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?title="(.*?)"'
                      +'.*?data-src="(.*?)".*?<p class="star">(.*?)</p>'
                      +'.*?<p class="releasetime">(.*?)</p>'
                       +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'
                      ,re.S)
    items =re.findall(pattern,html)
    #print(items)
    for item in items:
        yield{
            'index':item[0],
            'title': item[1],
            'image': item[2],
            'actors': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score':item[5]+item[6]

        }

#写入文件
def write_file(content):
    #a表示追加
    with open('maoyan.txt','a',encoding='utf-8') as f:
        #如果不带ensure_ascii=False，输出的是ascii码 例如："\u4e2d\u56fd"
        f.write(json.dumps(content,ensure_ascii=False)+'\n')


def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_file(item)


if __name__=='__main__':
    for i in range(10):

        main(offset=i*10)
        time.sleep(1)
    
