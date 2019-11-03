# Bilibili-Favorites-Download

![](https://img.shields.io/github/issues/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/forks/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/stars/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/license/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/languages/top/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/last-commit/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/languages/code-size/ColorfulMist/Bilibili-Favorites-Download)
![](https://img.shields.io/github/repo-size/ColorfulMist/Bilibili-Favorites-Download)

项目仍在开发中，目前仅完成`data.py`和`data_csv.py`部分。

这是一个用于下载bilibili弹幕视频网站个人收藏夹信息的爬虫，数据来源是bilibili官方网站的api和biliplus网站的api，目前支持保存成txt文本文件和可以使用Excel打开的csv逗号分隔符文件，会保存尽量多的信息种类，如有需求，可以自行对照api返回的信息进行修改。

这个项目的原始动力是我自己的的需求，如果在使用中遇到了困难和bug以及有对项目的意见，欢迎在Issues中提出，我将提供帮助和不断改进。

如果这个项目帮助了你，欢迎Star，您的Star是我继续维护与开发的动力。

## 使用

请首先将您需要爬取信息的bilibili收藏夹设为公开

### 使用python源代码

需要`Python3`环境

`data.py`是输出txt文件的代码

`data_csv.py`是输出csv文件的代码

在命令行下输入`python data.py`后

输入你的bilibili账号的uid，uid是web端个人主页网址url末尾的数字，或者可以自行查看bilibili个人信息

收藏夹信息文件会保存到当前目录

### 使用exe可执行文件

在release中提供`data.exe`及`data_csv.exe`

打开exe文件后输入bilibili账号的uid


## 开发计划

制作使用PyQt5的窗口程序，并开发选择保存文件路径，选择两种输出方式的功能。