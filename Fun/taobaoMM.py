# -*- coding:utf-8 -*-
import os
import re
import urllib2
import tool


class Spider:
    def __init__(self):
        self.siteUrl = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()

    def getPage(self, indexPage):
        url = self.siteUrl + "?page=" + str(indexPage)
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(
                '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?">(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
                re.S)
        items = re.findall(pattern, page)
        for item in items:
            print item[0] if item[0].__contains__('http:') else ('http:' + item[0]), item[1] if item[1].__contains__(
                    'http:') else ('http:' + item[1]), item[2], item[
                3], item[4]
            # self.saveImg(item[1] if item[1].__contains__(
            #         'http:') else ('http:' + item[1]), item[2])

    def saveImg(self, imgUrl, fileName):
        res = urllib2.urlopen(imgUrl)
        data = res.read()
        f = open(fileName, "wb")
        f.write(data)
        print u"正在悄悄保存她的一张图片为", fileName
        f.close()

    def saveBrief(self, content, name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName, "w+")
        print u"正在偷偷的保存她的个人信息为", fileName
        f.write(content.encode('utf-8'))

    def mkidr(self, path):
        path = path.strip()
        isExits = os.path.exists(path)
        if not isExits:
            os.mkdir(path)
            return True
        else:
            return False

    # 获取MM个人详情页
    def getDetailsPage(self, infoUrl):
        response = urllib2.urlopen(infoUrl)
        return response.read().decode('gbk')

    # 获取个人文字简介
    def getBrief(self, page):
        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        result = re.search(pattern, page)
        return self.tool.replace(result)

    def getAllImg(self, page):
        pattern = re.compile('<div class="mm-aiiu-content".*?>(.*?)<!--')
        # 个人信息页面所有代码
        content = re.search(pattern, page)
        # 从代码中提取图片
        patternImg = re.compile('<img.*?src="(.*?)"', re.S)
        images = re.findall(patternImg, content.group(1))
        return images


spider = Spider()
spider.getContents(1)
