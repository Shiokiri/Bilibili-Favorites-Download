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
    print('收藏夹编号,收藏夹名称,收藏夹视频数量,视频编号,AV号,视频状态,视频标题,封面图片,投稿时间,描述,分区,标签,up主用户名,up主uid,播放,弹幕,回复,收藏,硬币,分享,喜欢,收藏时间,')
    favoriteListUrl = 'https://api.bilibili.com/x/space/fav/nav?mid={uid}&jsonp=jsonp'.format(uid=uid)
    favoriteListData = getJsonUrl(favoriteListUrl)
    listInfo = favoriteListData['data']['archive']
    favNum = len(listInfo)
    for i in range(0, favNum):
        totVideoNum += listInfo[i]['cur_count']
    for i in range(0, favNum):
        favInformation = '#{x1},{x2},{x3}'.format(x1=i+1, x2=listInfo[i]['name'], x3=listInfo[i]['cur_count'])
        getFavListVideo(uid, listInfo[i]['fid'], favInformation)

def printInfo(Info):
    print(time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(Info['pubdate'])), end=',')
    print('"%s"' % (Info['desc']), end=',')
    print('"%s"' % (Info['tname']), end=',')
    print('"%s"' % (Info['dynamic']), end=',')
    print('"%s","%s"' % (Info['owner']['name'], Info['owner']['mid']), end=',')
    print('%s,%s,%s,%s,%s,%s,%s' % (Info['stat']['view'], Info['stat']['danmaku'], Info['stat']['reply'], Info['stat']['favorite'], Info['stat']['coin'], Info['stat']['share'], Info['stat']['like'],), end=',')
    print(time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(Info['fav_at'])), end=',')
    print()

def getFavListVideo(uid, fid, favInfo):
    global aFavVideoCnt, totVideoCnt, totVideoNum
    aFavVideoCnt = 0
    favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=30&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid, fid=fid, page=1)
    favPageDate = getJsonUrl(favPageUrl)
    printVideoInfo(favPageDate['data']['archives'], favInfo)
    pageCount = favPageDate['data']['pagecount']
    for i in range(2, pageCount+1):
        favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=30&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid, fid=fid, page=i)
        favPageDate = getJsonUrl(favPageUrl)
        printVideoInfo(favPageDate['data']['archives'], favInfo)

def printVideoInfo(aPageInfo, favInfo):
    global aFavVideoCnt, totVideoCnt, totVideoNum
    for i in range(0, len(aPageInfo)):
        print(favInfo, end=',')
        aFavVideoCnt += 1
        totVideoCnt += 1
        if totVideoCnt % 10 == 0 or totVideoCnt == totVideoNum: logging.info('已经完成了{num1}/{num2}个视频...'.format(num1=totVideoCnt, num2=totVideoNum))
        Info = aPageInfo[i]
        video_id = Info['aid']
        if Info['title'] == '已失效视频':
            getInvalidVideoInfo(video_id, Info)
        else:
            print('#%d,%d,[有效],"%s","%s"' % (aFavVideoCnt, Info['aid'], Info['title'], Info['pic']), end=',')
            printInfo(Info)

biliplusApiCnt = 0
runTime = 0

def getInvalidVideoInfo(video_id, Info):
    global aFavVideoCnt, biliplusApiCnt, runTime
    biliplusApiCnt += 1
    while biliplusApiCnt / ((time.clock() - runTime) / 60.0) >= 5: time.sleep(1)
    url = 'https://www.biliplus.com/api/view?id={vid}'.format(vid = video_id)
    InvVideoInfo = getJsonUrl(url)
    if 'code' in InvVideoInfo:
        print('#%d,%d,[失效][BiliplusApi数据缺失],已失效视频,(·w·)' % (aFavVideoCnt, Info['aid']), end=',')
        printInfo(Info)
    else:
        print('#%d,%d,有效,"%s","%s"' % (aFavVideoCnt, Info['aid'], InvVideoInfo['title'], InvVideoInfo['pic']), end=',')
        printInfo(Info)

def start(): # for cmd
    global totVideoNum
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