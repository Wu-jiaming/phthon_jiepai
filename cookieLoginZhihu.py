import requests

headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Cookie':'q_c1=67ff5741b83a4a6e86166c635fae02bf|1520254489000|1517571696000; _zap=079c17ac-ebbd-4c8b-8684-e50dec3a063a; l_cap_id="YmVhMWU0NjY0NjQwNDYxMWE5NWRhMzcyZDQ4ZjJhMmM=|1520855080|be363e11df6daec1927bec0afcfe98da5e099bb2"; r_cap_id="MGFiYTI4ZDc4MjEyNDQ5MDgxMTlmNzM1MmU5YTkwY2I=|1520855080|8646d5affdc401db3a7375a9c6d245d2fe4186cd"; cap_id="MzUyNGY2Y2E5ZGNkNDRkYzgwZDNhNWYxMDcwMWUzMmU=|1520855080|285e411e8f8a193565962be78a844572cd49f10a"; l_n_c=1; n_c=1; d_c0="AEArnWWVRg2PTgrZcquaIJp7sDN7YvI_Fto=|1520855083"; z_c0="2|1:0|10:1520857422|4:z_c0|92:Mi4xbl9NTUJBQUFBQUFBUUN1ZFpaVkdEU1lBQUFCZ0FsVk5Uci1UV3dER3Zpd3dHS1BoM1lsZUxSX1IydTdLOVI1WEZn|8407ba9557bfa309e6e91cc7edb827deb4670d42d4fa311e7696916a9f8a8a83"; aliyungf_tc=AQAAADbTgXiGIA0AEklJ391JudfM9zEL',
        'Host':'www.zhihu.com',
        'reference':'https://www.zhihu.com'
    }

r=requests.get("https://www.zhihu.com",headers=headers)
print(r.text)
