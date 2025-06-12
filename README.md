![longhtk](https://cdn.jsdelivr.net/gh/kanocyann/PicGo@master/20250505200512645.png)

# Hantokana

### 简介

这是一款由python语言开发的用于将日文汉字转换为假名和罗马音的工具

假名（日语：仮名／かな Kana ，日语发音：[kana]）为日本人创造的表音文字，与汉字共同构成日语的传统书写系统。

本应用不是中日互译词典，仅为拼写查询的小工具，所以没有很强的技术力，仅供娱乐Ciallo～(∠・ω＜)⌒☆

### 功能

1. 支持 **汉字->平假名<->片假名->罗马音**

2. 支持自定义词典

   ~~其实是汉字存在音读和训读两种情况，所以比较省事的办法是自己补充~~

3. 文件 - 词典导入功能会将你提供的json词库合并到默认词库中

   如果你想用自己的词库也可以在设置中指定默认词库位置

### 应用截图

主界面

![image-20250613001555080](https://cdn.jsdelivr.net/gh/kanocyann/PicGo@master/202506130016247.png)

词典编辑界面

![image-20250613001623017](https://cdn.jsdelivr.net/gh/kanocyann/PicGo@master/202506130016090.png)

### 下载与使用

一、下载Release中打包好的exe安装包进行安装，然后开始使用

二、本地环境启动

1. bash，cmd，powershell等shell

```shell
git clone https://github.com/kanocyann/hantokana.git
```

或者直接下载

![image-20250505195523371](https://cdn.jsdelivr.net/gh/kanocyann/PicGo@master/20250505195523425.png)

2. 然后执行

```shell
pip install -r requirements.txt
```

3. 启动程序

```shell
python hantokana.py
```

------

如果觉得这个工具好玩的话就点一个小STAR✨吧
