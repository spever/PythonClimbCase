# -*-coding:utf-8 -*-
import urllib2

# cookie = cookielib.CookieJar()
# handler = urllib2.HTTPCookieProcessor(cookie)
# opener = urllib2.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
#     print 'Name = ' + item.name;
#     print 'Value = ' + item.value;
import re


# filename = 'cookie.txt';
# cookie = cookielib.MozillaCookieJar(filename)
# handler = urllib2.HTTPCookieProcessor(cookie);
# opener = urllib2.build_opener(handler)
# response = opener.open("http://www.vc.cn")
# cookie.save(ignore_discard=True, ignore_expires=True)
# pat = re.compile(r'(\w+),(\w+)')
# s = 'i say,hello world!'
# print  re.sub(pat, r'\2 \1', s)
#
#
# def func(m):
#     return m.group(1).title() + ' ' + m.group(2).title()
#
#
# print re.sub(pat, func, s)



# page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
# headers = {"User-Agent": user_agent}
# try:
#     request = urllib2.Request(url, headers=headers)
#     response = urllib2.urlopen(request)
#     content = response.read().decode('utf-8')
#     pattern = re.compile(
#             'h2>(.*?)</h2.*?content">.*?<span.*?>(.*?)</span.*?number">(.*?)</', re.S)
#     items = re.findall(pattern, content)
#     for item in items:
#             print item[0], item[1],item[2]
# except urllib2.URLError, e:
#     if hasattr(e, "code"):
#         print e.code
#     if hasattr(e, "reason"):
#         print e.reason


class QSBK:
    # 初始化方法,定义一些变量
    def __init__(self):
        self.pageIndex = 1;
        self.user_agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的host
            request = urllib2.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为utf-8编码
            pageCode = response.read().decode('utf-8')

            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败......"
            return None

        pattern = re.compile(
                '<div.*?author.*?">.*?<h2>(.*?)</h2>.*?<div.*?' + 'content">.*?<span>(.*?)</span>.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',
                re.S)
        items = re.findall(pattern, pageCode)
        # 用来存储每页的段子
        pageStories = []
        # 遍历
        for item in items:
            haveImg = re.search("img", item[2])
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
                pageStories.append([item[0].strip(), text.strip(), item[3].strip()])

        return pageStories

    # 加载并提取页面的内容,加入到列表中...
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)

                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    # 调用该方法,每次敲回车打印输入一个段子
    def getOneStory(self, pageStories, page):

        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t好笑:%s\n%s" % (page, story[0], story[2], story[1])

    # 开始fangfa

    def start(self):
        print u"正在读取糗事百科,按回车查看新段子,Q退出"

        self.enable = True

        self.loadPage()

        nowPage = 0

        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]

                nowPage += 1

                del self.stories[0]

                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
