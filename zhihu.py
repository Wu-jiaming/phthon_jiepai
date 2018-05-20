import requests
import re

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

r=requests.get("https://www.zhihu.com/explore",headers=headers)

pattern=re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)

titles=re.findall(pattern,r.text)

print(titles)
