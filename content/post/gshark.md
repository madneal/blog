---
title: "GShark 重大重构重新发布"
author: Neal
tags: [开发,安全,应用安全,security,development,web security,chrome,cross-site,csrf]
categories: [安全]
date: "2021-02-17" 
---

GShark 作为一款开源的敏感信息监测工具其实差不多维护也有两年多的时间。这款产品其实笔者在自己的公司或者平常都在使用，也通过这个工具发现多多起内部的信息泄露事件以及外部的一些的信息泄露事件。其实这种类似的开源工具数不胜数，大家的核心功能其实就是监控 Github 上面的信息，但是笔者要想把这种产品做得更好一点，就要从功能性、易用性角度来做进一步拓展。最近，对 [GShark](https://github.com/madneal/gshark) 做了较大的重构，前后端都完成了比较大的重构，之前老的版本也有写过[文章](https://mp.weixin.qq.com/s/rKdz9V1Vx548FvPHwNBn0Q)介绍，所以关于这个工具的起源就不多介绍了，主要对这次重构和新的架构做介绍。

## 架构

目前 GShark 已经是一个前后端分离的项目，之前因为前端通过后端模板直接渲染的，所以在前端的功能性以及美观性都会差很多。新的重构是基于 [gin-vue-admin](https://github.com/flipped-aurora/gin-vue-admin)，技术栈是后端通过 gin 实现，前端通过 vue-elemment 来实现。

![](https://user-images.githubusercontent.com/12164075/114326875-58e1da80-9b69-11eb-82a5-b2e3751a2304.png)

所以架构主要就分为前端和后端两个部分，而后端则分为 web 服务以及敏感信息的扫描服务。新的架构具有以下特点：

* 细粒度的权限控制，更好的安全性，包括菜单的权限设置以及 API 的权限设置
* 丰富的前端功能，CRUD 更简单
* 搜索源和之前保持一致，支持 github, gitlab 以及 searchcode

## 部署

之前就有想使用 [GShark](https://github.com/madneal/gshark) 的同学来和我反映，其实之前的编译就已经很简单了。但是因为有些人不太熟悉 go，所以觉得编译还是有一些问题。这一次，笔者专门写了一个脚本来发布三个操作系统下的工具包，所以直接使用即可，开箱即用，即使你不安装 go 也无所谓。

```
rm -rf ./releases/*
cd web
npm run build
cd ../

# build for mac
cd server
GOOS=darwin GOARCH=amd64 go build 
cd ../releases
mkdir gshark_darwin_amd64
cd gshark_darwin_amd64
mv ../../server/gshark .
cp -rf ../../server/resource .
cp ../../server/config-temp.yaml config.yaml
cd ../../
cp -rf ./web/dist ./releases/gshark_darwin_amd64
7z a -r ./releases/gshark_darwin_amd64.zip ./releases/gshark_darwin_amd64/

# build for windows
cd server
GOOS=windows GOARCH=amd64 go build
cd ../releases
mkdir gshark_windows_amd64
cd gshark_windows_amd64
mv ../../server/gshark.exe .
cp -rf ../../server/resource .
cp ../../server/config-temp.yaml config.yaml
cd ../../
cp -rf ./web/dist ./releases/gshark_windows_amd64
7z a -r ./releases/gshark_windows_amd64.zip ./releases/gshark_windows_amd64/

# build for linux
cd server
GOOS=linux GOARCH=amd64 go build -o gshark
cd ../releases
mkdir gshark_linux_amd64
cd gshark_linux_amd64
mv ../../server/gshark .
cp -rf ../../server/resource .
cp ../../server/config-temp.yaml config.yaml
cd ../../
cp -rf ./web/dist ./releases/gshark_linux_amd64
7z a -r ./releases/gshark_linux_amd64.zip ./releases/gshark_linux_amd64


rm -rf ./releases/gshark*/
```

这个是 build 的脚本，主要是实现跨平台的编译并且将前端文件夹打包进去，然后拿到这个安装包解压即可使用。目前 GShark 的发布应该只需要两个前提条件：

* nginx （其实这个不需要也可以，主要是为了将前端文件发布）
* mysql（目前仅支持 mysql）

### 发布步骤

Step 1:

下载[压缩包](https://github.com/madneal/gshark/releases)，然后将压缩包解压。

Step 2:

修改二进制文件的权限，以 [ghsark_darwin_amd64](https://github.com/madneal/gshark/releases/download/v0.7/gshark_darwin_amd64.zip)为例，解压后修改二进制文件权限 `chmod +x gshark`，然后启动服务 `./gshark web`。

Step 3:

将前端文件发布到 nginx 的根目录下，就是将压缩包内的 dist 文件夹的文件拷贝到 nginx 根目录下，另外为了反向代理后端服务还需要修改一下 nginx 的配置，加入以下配置：

```
location /api/ {
proxy_set_header Host $http_host;
proxy_set_header  X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
rewrite ^/api/(.*)$ /$1 break;
proxy_pass http://127.0.0.1:8888;
}
```

这样启动完 nginx 后，整个发布过程就完成了，关于整个发布流程，笔者也在B站上发布了一个[教学视频](https://www.bilibili.com/video/BV1Py4y1s7ap/)，如果感兴趣的还可以再去看看。

## 使用

如果其实之前使用过 GShark 的用户，对于功能的使用应该有多了解，这里着重介绍一些增加的功能。在上面的发布完成之后，第一次进入应用 `http://localhost:8080`，会需要初始化数据库，只要输入数据库用户名、密码以及数据库名即可。进入系统，首先是服务器运行状态的监控界面。系统主要分为几个菜单，当然有一些可能还是有冗余，后续可能会考虑删除掉，其实核心功能主要就是搜索结果、管理、以及超级管理员菜单。

[![server](https://z3.ax1x.com/2021/04/17/c4Lyh6.png)](https://imgtu.com/i/c4Lyh6)

和之前一样，如果需要开启 scan 服务，那么首先需要添加 Github 或者 Gitlab 的 token，这个可以在 token管理菜单下进行添加。另外也需要根据自己的需求在规则管理里添加规则：

![rule.png](https://i.loli.net/2021/04/17/SusckilMNTXYv3E.png)


当然你也可以配置过滤规则，主要是文件夹后缀的过滤，以及选择是否搜索 fork 的代码仓库。另外值得讲的就是角色管理，通过角色管理可以创建任意角色，每种角色对应的菜单权限或者 API 权限都可以自由设置

![role.gif](https://i.loli.net/2021/04/17/wkVgoAlPMSFXThv.gif)

关于这个系统的整体介绍也可看笔者在B站发布的这个[视频](https://www.bilibili.com/video/BV17f4y1p7za/)。

## 总结

目前基于新的框架做的重构对于前端方面说可以说是做了非常大的改善，不管是在功能性上亦或是美观性都强了不少。另外，由于完善的权限控制，这也对于系统的控制性的加强也有帮助。同时，由于技术栈的基础，后续开发也会更加的便捷。后续的计划可能是增加更多的搜索源并且修复现在存在的一些小 BUG 吧。

## 404StarLink 2.0 - Galaxy

![](https://github.com/knownsec/404StarLink-Project/raw/master/logo.png)

GShark 是 404Team [星链计划2.0](https://github.com/knownsec/404StarLink2.0-Galaxy)中的一环，如果对 GShark 有任何疑问又或是想要找小伙伴交流，可以参考星链计划的加群方式。

- [https://github.com/knownsec/404StarLink2.0-Galaxy#community](https://github.com/knownsec/404StarLink2.0-Galaxy#community)


