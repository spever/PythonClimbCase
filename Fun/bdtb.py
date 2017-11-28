# -*- coding:utf-8 -*-
import re
import urllib2


class BDTB:
    # http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1

    # 1 http://  代表资源传输使用http协议

    # 2 tieba.baidu.com 是百度的二级域名，指向百度贴吧的服务器。

    # 3 /p/3138733512 是服务器某个资源，即这个帖子的地址定位符

    # 4 see_lz和pn是该URL的两个参数，分别代表了只看楼主和帖子页码，等于1表示该条件为真
    def __init__(self, baseUrl, seeLz):
        self.baseUrl = baseUrl
        self.seeLz = '?see_lz=' + str(seeLz)

    def getPageResponse(self, page):
        try:
            url = self.baseUrl + self.seeLz + "&pn=" + str(page)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read()
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接百度贴吧失败,错误原因:", e.reason
                return None

    def getTitle(self):
        pageResponse = self.getPageResponse(1)
        pattern = re.compile('h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</',re.S)
        result = re.search(pattern,pageResponse)
        if  result:
            print result.group(1)

            return result.group(1).strip()
        else:
            return None

    def getPageNum(self):
        pageResponse = self.getPageResponse(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result= re.search(pattern,pageResponse)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

    def getReplyNumSm(self):
        pageResponse = self.getPageResponse(1)
        pattern = re.compile('<li class="l_reply_num.*?<span.*?>(.*?)</span>',re.S)
        result= re.search(pattern,pageResponse)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

baseUrl = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseUrl, 1)
bdtb.getTitle()
bdtb.getPageNum()
bdtb.getReplyNumSm()
