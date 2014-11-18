# 简介

这个repository里存的是自己平常写的一些小脚本。

## [lan_abuse_detector] (lan_abuse_detector) 局域网入侵检测
写这个脚本是意外发现家里的无线路由器密码貌似被人破解了，但是别人并不总是在网上，所以我需要写个脚本在后台crontab里定期跑，来检测由DHCP自动分配的IP地址，检测到之后将会进行端口扫描并将结果发送到我的邮箱里，并启动一个tcpdump进程在后台进行抓包，等我抓到他的信息后就要让他后悔。
依赖的开源软件：
* mutt 用来发送邮件
* nmap 用来扫描网络以及对主机进行端口扫描
* tcpdump 用来抓包
* ISC DHCP Server 这个脚本读取DHCP Server的配置文件，找到固定分配的IP地址，并在nmap发现的主机里进行排除

## [webcam](webcam) 摄像头入侵检测
这个bash脚本用来将家里的普通摄像头变成一个带入侵检测功能的安防系统。详细说明参考我的博客 [使用BASH来实现一个简单的摄像头运动检测监控程序](http://chou.it/2014/02/bash-web-camera-capture-and-motion-detect/)

依赖的开源软件：
* mplayer 这软件不只是是一个播放器，webcam脚本使用这个进行摄像头捕捉
* imagemagick 这个软件提供命令行接口的图像处理能力
* mutt 发送邮件
