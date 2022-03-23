# Bilibili-Favorites-Download

![](https://img.shields.io/github/issues/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/forks/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/stars/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/license/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/languages/top/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/last-commit/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/languages/code-size/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/repo-size/ColorfulMist/Bilibili-Favorites-Download)

这是一个用于下载bilibili弹幕视频网站个人收藏夹信息的爬虫，数据来源是bilibili网站的api数据和biliplus网站的api数据，支持保存成txt文本文件和可以使用Excel打开的csv逗号分隔符文件。

为了恢复失效视频，尝试使用biliplus的api获取标题和封面图片，因为biliplus的api要求一分钟访问量不大于5次，所以不得不在查询失效视频时人为限制了速度。

目前api出现问题，计划修复中。

## 效果

![](https://cdn.jsdelivr.net/gh/ShioKiri/cdn/img/1.png)

![](https://cdn.jsdelivr.net/gh/ShioKiri/cdn/img/2.png)

## 使用

请首先将您需要获取信息的bilibili收藏夹设为公开

### 使用python源代码

需要`Python3`环境

`data.py`是输出txt文件的代码

`data_csv.py`是输出csv文件的代码

在命令行下切换到代码文件目录，输入`python data.py`运行代码

输入你的bilibili账号的uid，uid是web端个人主页网址url末尾的数字，或者可以自行查看bilibili个人信息

收藏夹信息文件会保存到当前目录

### 使用exe可执行文件

在release中提供`data.exe`及`data_csv.exe`

因为release在国内下载不方便，所以我将exe一并上传至repo了

打开exe文件后输入bilibili账号的uid
