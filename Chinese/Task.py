# -*- coding:utf-8 -*-
import os
import urllib2

from Fun import tool

DIR_PATH = '/Users/luo/case/py/Chinese'


# start 22430 end 23142   25203---25254

class TaoBaoMM:
    def __init__(self):
        self.isUseCount = 1
        self.preCount = 0
        self.tool = tool.Tool()
        self.index = 'ls'
        self.siteUrl = 'http://d.yuwenziyuan.com/rjb/UploadFile/dzkb/'
        self.picUrl = 'http://d.yuwenziyuan.com/rjb/UploadFile/dzkb/1s/005.jpg'
        self.pageIndex = 22430
        self.validUrl = True
        self.is1s = True
        self.is1x = True
        self.is2s = True
        self.is2x = True
        self.is3s = True
        self.is3x = True
        self.is4s = True
        self.is4x = True
        self.is5s = True
        self.is5x = True
        self.is6s = True
        self.is6x = True
        self.imgs = []

    def on_start(self):
        global index
        while self.pageIndex <= 23142:

            print u"运行中...."
            self.pageIndex += 1

            if self.pageIndex >= 23078:
                if self.is6x:
                    self.is6x = False
                self.index = '6x'
                self.validUrl = True
                self.isUseCount = 12

            elif self.pageIndex >= 23016:
                if self.is6s:
                    self.is6s = False
                self.index = '6s'
                self.validUrl = True
                self.isUseCount = 11

            elif self.pageIndex >= 22952:
                if self.is5x:
                    self.is5x = False
                self.index = '5x'
                self.validUrl = True
                self.isUseCount = 10

            elif self.pageIndex >= 22887:
                if self.is5s:
                    self.is5s = False
                self.index = '5s'
                self.validUrl = True
                self.isUseCount = 9

            elif self.pageIndex >= 22828:
                if self.is4x:
                    self.is4x = False
                self.index = '4x'
                self.validUrl = True
                self.isUseCount = 8

            elif self.pageIndex >= 22767:
                if self.is4s:
                    self.is4s = False
                self.index = '4s'
                self.validUrl = True
                self.isUseCount = 7

            elif self.pageIndex >= 22708:
                if self.is3x:
                    self.is3x = False
                self.index = '3x'
                self.validUrl = True
                self.isUseCount = 6

            elif self.pageIndex >= 22649:
                if self.is3s:
                    self.is3s = False
                self.index = '3s'
                self.validUrl = True
                self.isUseCount = 5

            elif self.pageIndex >= 22596:
                if self.is2x:
                    self.is2x = False
                self.index = '2x'
                self.validUrl = True
                self.isUseCount = 4

            elif self.pageIndex > 22535:
                if self.is2s:
                    self.is2s = False
                self.index = '2s'
                self.validUrl = True
                self.isUseCount = 3

            elif self.pageIndex >= 22484:
                if self.is1x:
                    self.is1x = False
                self.index = '1x'
                self.validUrl = True
                self.isUseCount = 2

            elif self.pageIndex >= 22429:
                if self.is1s:
                    self.is1s = False
                self.index = '1s'
                self.validUrl = True
                self.isUseCount = 1

            if self.validUrl:
                if self.isUseCount != self.preCount:
                    self.preCount = self.isUseCount
                    for i in range(1, 201):
                        if i < 10:
                            index = '00' + str(i)
                        elif i < 100:
                            index = '0' + str(i)
                        elif i < 200:
                            index = str(i)

                        self.url = self.siteUrl + self.index + '/' + str(index) + '.jpg'

                        self.imgs.append(self.url)

            print self.url, u"运行到", self.pageIndex

    def saveImgs(self, images, name):
        number = 1
        print u"发现", name, u"共有", len(images), u"张图片"
        for imageUrl in images:
            splitPath = imageUrl.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            number += 1

            if os.path.exists(fileName):
                continue
            print imageUrl
            try:
                res = urllib2.urlopen(imageUrl)
                data = res.read()
                self.saveUrlImg(data, fileName)

                print u"正在悄悄保存她的一张图片为", fileName
            except urllib2.HTTPError, e:
                if hasattr(e, "reason"):
                    print(e.reason)
                number -= 1
                continue

    # 传入图片地址,文件名,保存单张图片
    def saveImg(self, imgUrl, fileName):

        global data
        try:
            res = urllib2.urlopen(imgUrl)
            data = res.read()
            print u"正在悄悄保存她的一张图片为", fileName
        except urllib2.HTTPError, e:
            if hasattr(e, "reason"):
                print(e.reason)

        f = open(fileName, "wb")
        f.write(data)

        if f is not None:
            f.close()

    # 传入图片地址,文件名,保存单张图片
    def saveUrlImg(self, data, fileName):

        f = open(fileName, "wb")
        f.write(data)

        if f is not None:
            f.close()

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
    def savePageInfo(self):
        self.mkdir(DIR_PATH)

        self.on_start()

        # 保存图片
        self.saveImgs(self.imgs, DIR_PATH)


taobaoModel = TaoBaoMM()
taobaoModel.savePageInfo()
