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
    return Data

def getFavoriteList(uid):
    global Favorite_id, Favorite_name, Fav_tot
    favoriteListUrl = 'https://api.bilibili.com/x/space/fav/nav?mid={uid}&jsonp=jsonp'.format(uid=uid)
    favoriteListData = getJsonUrl(favoriteListUrl)
    listInfo = favoriteListData['data']['archive']
    Fav_tot = len(listInfo)
    for i in range(0, Fav_tot):
        Favorite_id.append(listInfo[i]['fid'])
        Favorite_name.append(listInfo[i]['name'])
        print('收藏夹编号:%d fid:%d 收藏夹名称:%s 收藏夹视频数量' % (i+1, Favorite_id[i] ,Favorite_name[i], listInfo[i]['cur_count']))
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
        if aPageInfo[i]['title'] == '已失效视频':
            gitInvalidVideoInfo(aPageInfo[i]['aid'])
        else:
            print('%d %d %s' % (aFavCnt, aPageInfo[i]['aid'],aPageInfo[i]['title']))

def gitInvalidVideoInfo(video_id):
    global aFavCnt
    url = 'https://www.biliplus.com/api/view?id={vid}'.format(vid=video_id)
    InvVideoInfo = getJsonUrl(url)
    if 'code' in InvVideoInfo:
        print('%d %d [已失效][BiliplusApi数据缺失] 已失效视频' % (aFavCnt, video_id))
        return
    print('%d %d [已失效][BiliplusApi获得数据] %s' % (aFavCnt, video_id, InvVideoInfo['title']))


def Start():
    initUid()
    fo = open("FavoriteVideoList.txt", 'w', encoding = 'utf-8')
    getFavoriteList(bilibili_uid)
    fo.close()

if __name__ == '__main__':
    Start()