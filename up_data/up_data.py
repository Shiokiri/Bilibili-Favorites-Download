from urllib.request import urlopen
import json
import re
import time
import sys
import logging
# -*- coding: UTF-8 -*-

bilibili_uid = 0
totVideoNum = 0
completeVideoNum = 0

def initUid():
    global bilibili_uid
    logging.info('请输入bilibili用户uid：')
    bilibili_uid = int(input())

def getJsonUrl(url):
    Data = urlopen(url).read().decode('utf-8')
    jsonData = json.loads(Data)
    return jsonData

def getUpVideoList(uid):
    global totVideoNum, completeVideoNum, TypeName
    ListUrl = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize={page_size}&page={page_number}'.format(mid=uid,page_size=100,page_number=1)
    upData = getJsonUrl(ListUrl)
    pageNum = upData['data']['pages']
    totVideoNum = upData['data']['count']
    print('up主共有%s个视频\n' % (totVideoNum))
    printPage(upData['data']['vlist'])
    for i in range(2, pageNum+1):
        ListUrl = 'http://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize={page_size}&page={page_number}'.format(mid=uid,page_size=100,page_number=i)
        upData = getJsonUrl(ListUrl)
        printPage(upData['data']['vlist'])

def printPage(listInfo):
    global totVideoNum, completeVideoNum
    listLen = len(listInfo)
    for i in range(0, listLen):
        completeVideoNum += 1
        printInfo(listInfo[i])
        logging.info('已经完成了{num1}/{num2}个视频...'.format(num1 = completeVideoNum,num2 = totVideoNum))

def printInfo(Info):
    global completeVideoNum
    print('编号:#{id} AV号:{vid}'.format(id=completeVideoNum, vid=Info['aid']))
    print('标题:{title}'.format(title=Info['title']))
    print('投稿时间:' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(Info['created'])))
    print('封面:%s' % (Info['pic']))
    print('描述:%s' % (Info['description']))
    print('视频长度:%s' % (Info['length']))
    print('分区类型:%s' % (Info['typeid']))
    print('播放:%s  弹幕:%s  评论:%s  收藏:%s' % (Info['play'], Info['video_review'], Info['comment'], Info['favorites']))
    print()

def start(): # for cmd
    global totVideoNum
    logging.basicConfig(level=logging.DEBUG)
    if sys.getdefaultencoding() == 'ascii':
        sys.stdout = open("UpVideoList.txt", "w", encoding = 'gb2312')
    else:
        sys.stdout = open("UpVideoList.txt", "w", encoding = 'utf-8')
    initUid()
    getUpVideoList(bilibili_uid)
    logging.info('完事了！')

# def windowMain(Uid, filePath): # for window ui


if __name__ == '__main__': # cmd
    start()