from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as py
import json

class TZ:
    #初始化。seeLZ只看楼主
    def __init__(self,baseUrl,seeLZ,floorTag):
        self.baseUrl = baseUrl
        self.seeLZ = seeLZ
        self.floorTag = floorTag#表示楼层之间的间隔符
        self.file = None#表示将要写入的文件
        self.browser = self.phantomJS()
        self.floor = '1' #表示楼层数


    def phantomJS(self):
        # 禁止设置缓存和禁用图片
        SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
        browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        return browser

    def get_url(self,pageNum):
        if self.seeLZ == '1':
            url = self.baseUrl + '?see_lz=' + str(self.seeLZ) + '&pn=' + str(pageNum)
        else:
            url = self.baseUrl + '&pn=' + str(pageNum)
        return url

    def get_maxPageIndex(self):
        url = self.get_url(1)
        self.browser.get(url)
        doc = self.get_parse_page()
        maxPageIndex = doc('#thread_theme_5 .red').text().split(' ',1)[1]
        print(maxPageIndex)
        return  maxPageIndex

    def getPage(self,pageNum):
        """
        抓取索引页
        :param pageNum: 页码
        :return: 
        """
        print('正在爬去第',pageNum,'页')
        try:
            url = self.get_url(pageNum)
            self.browser.get(url)

            print(url)
            self.get_tiezi()
        except TimeoutException:
            print('爬取第',pageNum,'页失败')




    def get_parse_page(self):
        """
        获取解析网页
        :return: 
        """
        html = self.browser.page_source
        doc = py(html)

        return doc

    def get_title(self):
        """
        获取标题
        :return: 
        """
        doc = self.get_parse_page()
        title = doc('#j_core_title_wrap h3').text()
        return  title




    def get_tiezi(self):
        """
        抓取帖子内容
        :return: 
        """
        doc = self.get_parse_page()
        pageIndex = doc('#thread_theme_5 .red').text()
        items = doc('#pb_content .left_section .p_postlist .l_post.l_post_bright.j_l_post.clearfix  ').items()
        title = self.get_title()
        author_image = doc('#j_p_postlist .d_author .icon_relative.j_user_card .p_author_face img').attr('src')
        author = (doc('#j_p_postlist .d_author .d_name a').text()).split()[0]

        if  title is not None:
            file_name = title + '.txt'
            with open(file_name, 'a', encoding='utf-8') as f:
                f.write('标题：' + title +'\n')
                f.write('author：' + author + '\n')
                f.write('author_image：' + author_image + '\n')

        else:
            print('无法获取帖子标题')

        for item in items:
            tiezi={
                    'content':item.find('.d_post_content.j_d_post_content ').text()
            }
            self.writeData(tiezi)
            print('帖子内容：',tiezi)



        print('标题：',title,'\n','作者：',author,'\n','作者头像：',author_image,'\n')
        #print('标题：', title, '\n')
        print('pageindex',pageIndex)




    def writeData(self,item):
        """
        保存每一层的帖子内容 
        :param item:每一层的帖子内容 
        :return: 
        """
        if self.floorTag == '1':
            #楼之间的间隔符
            floorLine =  str(self.floor) + u"楼-------------------------------------" +"\n"

        title = self.get_title()+'.txt'
        with open(title,'a',encoding='utf-8') as f:
            f.write(floorLine)
            f.write(json.dumps(item,ensure_ascii=False)+'\n')
            self.floor = int(self.floor) + 1

    def start(self):
        print('开始读取帖子....')
        MaxIndex = int(self.get_maxPageIndex())+1
        for i in range(1,MaxIndex):
            self.getPage(i)


tiezi_num = input('请输入要抓取的帖子的特定号码：')
see_lz = input('是否只查看楼主的帖子，是则输入1，否则输入其他：')
floor_tag = input('是否在每个帖子输入间隔------------，是则输入1，否则输入其他:')
tz = TZ('https://tieba.baidu.com/p/'+tiezi_num,see_lz,floor_tag)
#tz = TZ('https://tieba.baidu.com/p/3138733512','1','1')
#tz.get_maxPageIndex()
tz.start()
