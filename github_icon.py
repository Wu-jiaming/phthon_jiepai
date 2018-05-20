import requests

r=requests.get("http://github.com/favicon.ico")

with open('favicon.ico','wb') as f:
    f.write(r.content)
