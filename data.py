from urllib.request import urlopen
import json
import re
# -*- coding: UTF-8 -*-

bilibili_uid = 0
Favorite_id = []
Favorite_name = []
Fav_tot = 0

def initUid():
    global bilibili_uid
    bilibili_uid = int(input())

def getJsonUrl(url):
    Data = urlopen(url).read().decode('utf-8')
    jsonData = json.loads(Data)
    return jsonData

def getFavoriteList(uid):
    global Favorite_id, Favorite_name, Fav_tot
    favoriteListUrl = 'https://api.bilibili.com/x/space/fav/nav?mid={uid}&jsonp=jsonp'.format(uid=uid)
    favoriteListData = getJsonUrl(favoriteListUrl)
    listInfo = favoriteListData['data']['archive']
    Fav_tot = len(listInfo)
    for i in range(0, Fav_tot):
        Favorite_id.append(listInfo[i]['fid'])
        Favorite_name.append(listInfo[i]['name'])
        print('收藏夹编号:%d fid:%d 名称:%s 视频数量:%d\n' % (i+1, Favorite_id[i] ,Favorite_name[i], listInfo[i]['cur_count']))
        getFavListVideo(uid, Favorite_id[i])

aFavCnt = 0
totVideoCnt = 0

def getFavListVideo(uid, fid):
    global aFavCnt, totVideoCnt
    aFavCnt = 0
    favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=30&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=1)
    favPageDate = getJsonUrl(favPageUrl)
    printVideoInfo(favPageDate['data']['archives'])
    pageCount = favPageDate['data']['pagecount']
    for i in range(2, pageCount+1):
        favPageUrl = 'https://api.bilibili.com/x/space/fav/arc?vmid={uid}&ps=30&fid={fid}&tid=0&keyword=&pn={page}&order=fav_time&jsonp=jsonp'.format(uid=uid,fid=fid,page=i)
        favPageDate = getJsonUrl(favPageUrl)
        printVideoInfo(favPageDate['data']['archives'])
    totVideoCnt += aFavCnt

def printVideoInfo(aPageInfo):
    global aFavCnt
    for i in range(0, len(aPageInfo)):
        aFavCnt += 1
        video_id = aPageInfo[i]['aid']
        if aPageInfo[i]['title'] == '已失效视频':
            gitInvalidVideoInfo(video_id, aPageInfo[i])
        else:
            InvData = bilibiliVideoApi(video_id)
            print('视频编号：%d  AV号：%d  视频标题:%s' % (aFavCnt, aPageInfo[i]['aid'],aPageInfo[i]['title']))
            # print('封面图片:%s' % ())


def gitInvalidVideoInfo(video_id, Info):
    global aFavCnt
    url = 'https://www.biliplus.com/api/view?id={vid}'.format(vid=video_id)
    InvVideoInfo = getJsonUrl(url)
    if 'code' in InvVideoInfo:
        print('[已失效][BiliplusApi数据缺失] 视频编号：%d  AV号：%d  视频标题:已失效视频' % (aFavCnt, video_id))
        print('数据最后获取日期:%s' % (Info['lastupdate']))
        print('描述:%s' % (Info['desc']))
        print('封面图片:%s' % (Info['pic']))
        print('分区:%s' % (Info['tname']))
        print('标签:%s' % (Info['dynamic']))
        print('up主用户名:%s up主uid:%s' % (Info['owner']['name'], Info['owner']['mid']))
        print('投稿时间:%s' % (Info['ctime']))
        print('播放:%s 弹幕:%s 回复:%s 收藏:%s 硬币:%s 分享:%s 喜欢:%s' % (Info['v2_app_api']['stat']['view'], Info['v2_app_api']['stat']['danmaku'], Info['v2_app_api']['stat']['reply'], Info['v2_app_api']['stat']['favorite'], Info['v2_app_api']['stat']['coin'], Info['v2_app_api']['stat']['share'], InvVideoInfo['v2_app_api']['stat']['like'],))
        print('收藏日期%s' % (Info['fav_at']))
        print()
        input()
        return
    print('[已失效][BiliplusApi获得数据] 视频编号：%d  AV号：%d  视频标题：%s' % (aFavCnt, video_id, InvVideoInfo['title']))
    print('数据最后获取日期:%s' % (InvVideoInfo['lastupdate']))
    print('描述:%s' % (InvVideoInfo['description']))
    print('封面图片:%s' % (InvVideoInfo['pic']))
    print('分区:%s' % (InvVideoInfo['typename']))
    print('标签:%s' % (InvVideoInfo['tag']))
    print('up主用户名:%s up主uid:%s' % (InvVideoInfo['author'], InvVideoInfo['mid']))
    print('投稿时间:%s' % (InvVideoInfo['created_at']))
    print('播放:%s 弹幕:%s 回复:%s 收藏:%s 硬币:%s 分享:%s 喜欢:%s' % (InvVideoInfo['v2_app_api']['stat']['view'], InvVideoInfo['v2_app_api']['stat']['danmaku'], InvVideoInfo['v2_app_api']['stat']['reply'], InvVideoInfo['v2_app_api']['stat']['favorite'], InvVideoInfo['v2_app_api']['stat']['coin'], InvVideoInfo['v2_app_api']['stat']['share'], InvVideoInfo['v2_app_api']['stat']['like'],))
    print('收藏日期%s' % (Info['fav_at']))
    print()

def bilibiliVideoApi(video_id):
    url = 'https://api.bilibili.com/x/article/archives?ids={uid}'.format(uid=video_id)
    videoInfo = getJsonUrl(url)
    return videoInfo


def start(): # for cmd
    initUid()
    fileWrite = open("FavoriteVideoList.txt", 'w', encoding='utf-8')
    getFavoriteList(bilibili_uid)
    fileWrite.close()

# def windowMain(Uid, filePath): # for window ui


if __name__ == '__main__': # cmd
    start()