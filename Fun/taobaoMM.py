# -*- coding:utf-8 -*-
import os
import re
import urllib2
import tool


class TaoBaoMM:
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
                '<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
                re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            print item[0] if item[0].__contains__('https?:') else ('http:' + item[0]), item[1] if item[1].__contains__(
                    'https?:') else ('http:' + item[1]), item[2] if item[2].__contains__('https?:') else (
                'http:' + item[2]), item[
                3], item[4], item[5]
            # self.saveImg(item[1] if item[1].__contains__(
            #         'http:') else ('http:' + item[1]), item[2])
            contents.append([item[0] if item[0].__contains__('https?:') else ('http:' + item[0]),
                             item[1] if item[1].__contains__(
                                     'https?:') else ('http:' + item[1]),
                             item[2] if item[2].__contains__('https?:') else (
                                 'http:' + item[2]), item[
                                 3], item[4], item[5]])
        return contents

    # 获取MM个人详情页
    def getDetailsPage(self, infoUrl):

        response = urllib2.urlopen(infoUrl)

        return response.read().decode('gbk')

    # 获取model域名地址
    def getModelHost(self, page):
        pattren = re.compile('<div class="mm-p-info mm-p-domain-info".*?<span>(.*?)</span>', re.S)
        result = re.search(pattren, page)
        return result

    # 获取个人文字简介
    def getBrief(self, page):

        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)

        result = re.search(pattern, page)
        return self.tool.replace(result)

    def getAllImg(self, page):

        pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--')

        # 个人信息页面所有代码
        content = re.search(pattern, page)
        # 从代码中提取图片
        patternImg = re.compile('<img.*?src="(.*?)"', re.S)
        images = re.findall(patternImg, content.group(1))
        return images

    def saveImgs(self, images, name):
        number = 1
        print u"发现", name, u"共有", len(images), u"张图片"
        for imageUrl in images:
            splitPath = imageUrl.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageUrl, fileName)
            number += 1

    # 保存头像
    def saveIcon(self, iconUrl, name):

        spiltPath = iconUrl.split('.')

        fTail = spiltPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconUrl, fileName)

    # 传入图片地址,文件名,保存单张图片
    def saveImg(self, imgUrl, fileName):

        res = urllib2.urlopen(imgUrl)

        data = res.read()
        f = open(fileName, "wb")
        f.write(data)
        print u"正在悄悄保存她的一张图片为", fileName
        f.close()

    # 保存个人简介
    def saveBrief(self, content, name):

        fileName = name + "/" + name + ".txt"

        f = open(fileName, "w+")
        print u"正在偷偷的保存她的个人信息为", fileName
        f.write(content.encode('utf-8'))

    # 创建新目录
    def mkdir(self, path):

        path = path.strip()

        isExits = os.path.exists(path)
        if not isExits:
            print u"偷偷创建了名字叫做", path, u"的文件夹"
            os.mkdir(path)
            return True
        else:
            print u"名为", path, "的文件夹已经创建成功"
            return False

    # 讲一页淘宝MM的信息保存起来
    def savePageInfo(self, pageIndex):
        # 获取第一页淘宝MM列表
        contents = self.getContents(pageIndex)
        for item in contents:
            # item[0]个人作品详情URL,item[1]头像URL,item[2]个人详情,item[3]姓名,item[4]年龄,item[5]居住地
            print u"发现一位模特,名字叫", item[3], u"芳龄", item[4], u"她在", item[5]
            print u"正在偷偷的保存", item[3], "的信息"
            print u"又意外得发现了她的个人地址是", item[2]
            # 个人详情页面的URL
            detailUrl = item[2]
            # 得到个人详情页面的代码
            detailPage = self.getDetailsPage(detailUrl)

            detailModel = self.getModelHost(detailPage);
            # 获取个人简介
            brief = self.getBrief(detailModel)
            # 获取所有图片列表
            images = self.getAllImg(detailModel)
            self.mkdir(item[3])
            # 保存个人简介
            self.saveBrief(brief, item[3])
            # 保存头像
            self.saveIcon(item[2], item[3])
            # 保存图片
            self.saveImgs(images, item[3])

    def saveMMPagesInfo(self, start, end):
        for i in range(start, end + 1):
            print u"正在偷偷寻找第", i, u"个地方,看看MM们在不在"
            self.savePageInfo(i)


taobaoModel = TaoBaoMM()
taobaoModel.saveMMPagesInfo(1, 10)
