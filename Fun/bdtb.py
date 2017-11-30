# -*- coding:utf-8 -*-
import re
import urllib2


class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|></a>')
    # 把换行的标签换为\n
    removeLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加两空格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.removeLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n   ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)

        return x.strip()


class BDTB:
    # http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1

    # 1 http://  代表资源传输使用http协议

    # 2 tieba.baidu.com 是百度的二级域名，指向百度贴吧的服务器。

    # 3 /p/3138733512 是服务器某个资源，即这个帖子的地址定位符

    # 4 see_lz和pn是该URL的两个参数，分别代表了只看楼主和帖子页码，等于1表示该条件为真
    def __init__(self, baseUrl, seeLz, floorTag):
        self.baseUrl = baseUrl
        self.seeLz = '?see_lz=' + str(seeLz)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        self.floorTag = floorTag

    def getPageResponse(self, page):
        try:
            url = self.baseUrl + self.seeLz + "&pn=" + str(page)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因:", e.reason
                return None

    # 获取帖子标题
    def getTitle(self, pageRes):
        pattern = re.compile('h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</', re.S)
        result = re.search(pattern, pageRes)
        if result:
            print result.group(1)

            return result.group(1).strip()
        else:
            return None

    # 获取该帖子一共多少页
    def getPageNum(self, pageRes):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, pageRes)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

    # 获取该帖子总共回复数量
    def getReplyNumSm(self):
        pageResponse = self.getPageResponse(1)
        pattern = re.compile('<li class="l_reply_num.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, pageResponse)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

    # 提取正文内容
    def getContent(self, pageRes):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, pageRes)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content.encode('utf-8'))
        return contents

    # 设置文件名标题
    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    # 写数据
    def wirteData(self, contents):

        for item in contents:
            if self.floorTag == '1':
                floorline = "\n" + str(
                        self.floor) + u"---------------------------------------------------------------\n"
                self.file.write(floorline)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPageResponse(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print "URL 已失效,请重试"
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1, int(pageNum) + 1):
                print  "正在写入第" + str(i) + "页数据"
                page = self.getPageResponse(i)
                contents = self.getContent(page)
                self.wirteData(contents)
        except IOError, e:
            print "写入异常,原因" + e.message
        finally:
            print "写入任务完成"


print u"请输入帖子代号"
baseUrl = 'https://tieba.baidu.com/p/' + str(raw_input(u'https://teiba.baidu.com/p/'))
seelz = raw_input("是否只获取楼主发言,是输入1,否输入0\n")
floorTag = raw_input("是否写入楼层信息,是输入1,否输入0\n")
bdtb = BDTB(baseUrl, seelz, floorTag)
bdtb.start()
