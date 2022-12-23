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

def getJsonUrl(url):
    Data = urlopen(url).read().decode('utf-8')
    jsonData = json.loads(Data)
    return jsonData

def getFavoriteList(uid):
    global totVideoNum
    favoriteListUrl = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all?' \
                      'pn=1&ps=100&up_mid={uid}&is_space=0&jsonp=jsonp'.format(uid=uid)
    favoriteListData = getJsonUrl(favoriteListUrl)
    listInfo = favoriteListData['data']['list']
    favNum = len(listInfo)
    for i in range(0, favNum):
        totVideoNum += listInfo[i]['media_count']
    for i in range(0, favNum):
        print('收藏夹编号:#%d 名称:%s 视频数量:%d\n' % (i + 1, listInfo[i]['title'], listInfo[i]['media_count']))
        getFavListVideo(listInfo[i]['id'], int(listInfo[i]['media_count'] / 20 + 1))

def getFavListVideo(media_id, pagecount):
    global aFavVideoCnt, totVideoCnt, totVideoNum
    aFavVideoCnt = 0
    for i in range(1, pagecount + 1):
        favPageUrl = 'https://api.bilibili.com/x/v3/fav/resource/list?' \
                     'ps=20&media_id={media_id}&tid=0&keyword=&pn={page}&order=mtime&jsonp=jsonp&platform=web'.format(
            media_id=media_id, page=i)
        favPageDate = getJsonUrl(favPageUrl)
        printVideoInfo(favPageDate['data']['medias'])

def printVideoInfo(aPageInfo):
    global aFavVideoCnt, totVideoCnt, totVideoNum
    for i in range(0, len(aPageInfo)):
        aFavVideoCnt += 1
        totVideoCnt += 1
        if totVideoCnt % 20 == 0 or totVideoCnt == totVideoNum:
            logging.info('已完成{num1}/{num2}个视频...'.format(num1=totVideoCnt, num2=totVideoNum))
        Info = aPageInfo[i]
        # video_id = Info['id']
        # if Info['title'] == '已失效视频':
        #     getInvalidVideoInfo(video_id, Info)
        # else:
        print('视频编号:#%d  av号:%d  视频标题:%s' % (aFavVideoCnt, Info['id'], Info['title']))
        print('封面图片:%s' % (Info['cover']))
        printInfo(Info)

def printInfo(Info):
    print('投稿时间:' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(Info['pubtime'])))
    print('描述:%s' % (Info['intro']))
    # print('分区:%s' % (Info['tname']))
    # print('标签:%s' % (Info['dynamic']))
    print('up主用户名:%s  up主uid:%s' % (Info['upper']['name'], Info['upper']['mid']))
    # print('播放:%s  弹幕:%s  回复:%s  收藏:%s  硬币:%s  分享:%s  喜欢:%s' % (
    #     Info['stat']['view'], Info['stat']['danmaku'], Info['stat']['reply'], Info['stat']['favorite'],
    #     Info['stat']['coin'], Info['stat']['share'], Info['stat']['like'],))
    print('播放:%s  弹幕:%s  收藏:%s' % (
        Info['cnt_info']['play'], Info['cnt_info']['danmaku'], Info['cnt_info']['collect']))
    print('收藏时间:' + time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(Info['fav_time'])))
    print()

biliplusApiCnt = 0
runTime = 0

def getInvalidVideoInfo(video_id, Info):
    global aFavVideoCnt, biliplusApiCnt, runTime
    biliplusApiCnt += 1
    while biliplusApiCnt / ((time.time() - runTime) / 60.0) >= 5: time.sleep(1)
    url = 'https://www.biliplus.com/api/view?id={vid}'.format(vid=video_id)
    InvVideoInfo = getJsonUrl(url)
    if 'code' in InvVideoInfo:
        print('视频编号:#%d  [已失效][BiliplusApi数据缺失]  AV号:%d  视频标题:已失效视频' % (aFavVideoCnt, video_id))
        print('封面图片:%s' % (Info['pic']))
        printInfo(Info)
    else:
        print(
            '视频编号:#%d  [已失效][BiliplusApi获得标题与封面图片]  AV号:%d  视频标题:%s' % (aFavVideoCnt, video_id, InvVideoInfo['title']))
        print('封面图片:%s' % (InvVideoInfo['pic']))
        printInfo(Info)

def start():
    global totVideoNum, runTime, bilibili_uid
    logging.basicConfig(level=logging.DEBUG)
    if sys.getdefaultencoding() == 'ascii':
        sys.stdout = open("FavoriteVideoList.txt", "w", encoding='gb2312')
    else:
        sys.stdout = open("FavoriteVideoList.txt", "w", encoding='utf-8')
    bilibili_uid = int(input())
    runTime = time.time()
    getFavoriteList(bilibili_uid)
    print('收藏夹共有%d个视频' % (totVideoNum))
    logging.info('完成')


if __name__ == '__main__':
    start()
