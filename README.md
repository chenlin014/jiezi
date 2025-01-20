# 新郑

此库源自对[郑码](https://baike.baidu.com/item/%E9%83%91%E7%A0%81/589192)的改造。

## 简介

本库提供两个制作输入法的模板。

`make`负责将拆字表和拆字规则转化成不同输入系统所用的编码辞典。`make`生成的编码会存进`build/`。

目前、拆字方案、字根码全方案、按式方案等都只有一个、将来可能会有别的选项。

## 码表

### 初拆表

#### 字形与字码

#### 问题

##### 输错码

##### 字码显示不出来

##### 拆解规则不一致

##### 不同的字体和写法

### 输入码

#### 转换过程

#### 兼容码

### 字集

### 常用字标准码

### 代码

### 简码

#### 生成过程

## 连击输入法

### 字根分区

### 根区布局与键盘布局

### 双码

### 新郑为例

## 并击输入法

### 按式表

### 并击系統

### 排序表

#### 罕见“简体字”问题

### 有熊为例

## Makefile

### 流程

## 输入方案
### 新郑
- Rime: https://github.com/chenlin014/rime-xingzheng
### 有熊
- Rime: https://github.com/chenlin014/rime-youxiong

## 感谢
### 郑码发明人
郑易里、郑珑。

### 参考资料
- [kfcd/chaizi](https://github.com/kfcd/chaizi)（漢語拆字字典）
- [百度百科](https://baike.baidu.com)
- 《汉字源流大字典》谷衍奎 编著。ISBN: 9787100216333

### 字频来源
- 正體：
    - [教育部語文成果網](https://language.moe.gov.tw/)
    - [字頻總表](https://language.moe.gov.tw/001/Upload/files/SITE_CONTENT/M0001/PIN/biau1.htm?open)
- 简体：
    - 北京语言大学，邢红兵 <xinghb@blcu.edu.cn>
    - [25亿字语料汉字字频表](https://faculty.blcu.edu.cn/xinghb/zh_CN/article/167473/content/1437.htm#article)
- 日文：
    - [文化庁](https://www.bunka.go.jp/)
    - [漢字出現頻度数調査](https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/nihongokyoiku_hyojun_wg/04/pdf/91934501_08.pdf)
