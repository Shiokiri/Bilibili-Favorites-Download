from urllib.request import urlopen
import json
import re
import time
import sys
import logging
# -*- coding: UTF-8 -*-

bilibili_uid = 0
aFavVideoCnt = 0
totVideoCnt = 0
totVideoNum = 0

def initUid():
    global bilibili_uid
    bilibili_uid = int(input())

def getJsonUrl(url):
    Data = urlopen(url).read().decode('utf-8')
    jsonData = json.loads(Data)
    return jsonData

def getFavoriteList(uid):
    global totVideoNum
    favoriteListUrl = 'https://api.bilibili.com/x/space/fav/nav?mid={uid}&jsonp=jsonp'.format(uid=uid)
    favoriteListData = getJsonUrl(favoriteListUrl)
    listInfo = favoriteListData['data']['archive']
    favNum = len(listInfo)
    for i in range(0, favNum):
        totVideoNum += listInfo[i]['cur_count']
    for i in range(0, favNum):
        print('收藏夹编号:#%d 名称:%s 视频数量:%d\n' % (i+1, listInfo[i]['name'], listInfo[i]['cur_count']))
        getFavListVideo(uid, listInfo[i]['fid'])

def getFavListVideo(uid, fid):
    global aFavVideoCnt, totVideoCnt, totVideoNum
    aFavVideoCnt = 0
    favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=30&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=1)
    favPageDate = getJsonUrl(favPageUrl)
    printVideoInfo(favPageDate['data']['archives'])
    pageCount = favPageDate['data']['pagecount']
    for i in range(2, pageCount+1):
        favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=30&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=i)
        favPageDate = getJsonUrl(favPageUrl)
        printVideoInfo(favPageDate['data']['archives'])

def printInfo(Info):
    print('投稿时间:' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(Info['pubdate'])))
    print('描述:%s' % (Info['desc']))
    print('分区:%s' % (Info['tname']))
    print('标签:%s' % (Info['dynamic']))
    print('up主用户名:%s  up主uid:%s' % (Info['owner']['name'], Info['owner']['mid']))
    print('播放:%s  弹幕:%s  回复:%s  收藏:%s  硬币:%s  分享:%s  喜欢:%s' % (Info['stat']['view'], Info['stat']['danmaku'], Info['stat']['reply'], Info['stat']['favorite'], Info['stat']['coin'], Info['stat']['share'], Info['stat']['like'],))
    print('收藏时间:' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(Info['fav_at'])))
    print()

def printVideoInfo(aPageInfo):
    global aFavVideoCnt, totVideoCnt, totVideoNum
    for i in range(0, len(aPageInfo)):
        aFavVideoCnt += 1
        totVideoCnt += 1
        if totVideoCnt % 10 == 0 or totVideoCnt == totVideoNum: logging.info('已经完成了{num1}/{num2}个视频...'.format(num1 = totVideoCnt,num2 = totVideoNum))
        Info = aPageInfo[i]
        video_id = Info['aid']
        if Info['title'] == '已失效视频':
            getInvalidVideoInfo(video_id, Info)
        else:
            print('视频编号:#%d  AV号:%d  视频标题:%s' % (aFavVideoCnt, Info['aid'], Info['title']))
            print('封面图片:%s' % (Info['pic']))
            printInfo(Info)

biliplusApiCnt = 0
runTime = 0

def getInvalidVideoInfo(video_id, Info):
    global aFavVideoCnt, biliplusApiCnt, runTime
    biliplusApiCnt += 1
    while biliplusApiCnt / ((time.clock() - runTime) / 60.0) >= 5: time.sleep(1)
    url = 'https://www.biliplus.com/api/view?id={vid}'.format(vid = video_id)
    InvVideoInfo = getJsonUrl(url)
    time.sleep(0.03)
    if 'code' in InvVideoInfo:
        print('视频编号:#%d  [已失效][BiliplusApi数据缺失]  AV号:%d  视频标题:已失效视频' % (aFavVideoCnt, video_id))
        print('封面图片:%s' % (Info['pic']))
        printInfo(Info)
    else:
        print('视频编号:#%d  [已失效][BiliplusApi获得标题与封面图片]  AV号:%d  视频标题:%s' % (aFavVideoCnt, video_id, InvVideoInfo['title']))
        print('封面图片:%s' % (InvVideoInfo['pic']))
        printInfo(Info)

def start(): # for cmd
    global totVideoNum, runTime
    logging.basicConfig(level=logging.DEBUG)
    if sys.getdefaultencoding() == 'ascii':
        sys.stdout = open("FavoriteVideoList.txt", "w", encoding = 'gb2312')
    else:
        sys.stdout = open("FavoriteVideoList.txt", "w", encoding = 'utf-8')
    initUid()
    runTime = time.clock()
    getFavoriteList(bilibili_uid)
    print('你的收藏夹共有%d个视频' % (totVideoNum))
    logging.info('完事了！')

# def windowMain(Uid, filePath): # for window ui


if __name__ == '__main__': # cmd
    start()