---
title: "Home Assistant 小米全屋智能"
author: Neal
tags: [全屋只能,小米]
categories: [生活]
date: "2024-06-29" 
---

小米的门铃，免费的云存储时间只有 72 小时，希望保存更多时间的视频，只能去充钱。后来网上搜了一下，通过 [Home Assistant](https://www.home-assistant.io/) 的小米插件可以实现这样的功能。刚好家里有一台闲置的 Macbook 用来发挥余热不是刚好。其实我之前已经安装好了，只不过手残把镜像文件删掉了，这样刚好出个教程从头来一次。

## Home Assistant 安装

Home Assistant 支持多种安装方案，不过他们主推的是他们自己的一款软硬件一体的方案。其实家里是有一台软路由的，不过软路由担心把网络搞出问题，还是选择使用那台闲置的 Mac。官网里面也包含了 MacOS 的[安装方案](https://www.home-assistant.io/installation/macos)。因为 Home Assistant 用的是比较低版本的 Linux 系统，所以基本都还是需要使用虚拟机。首先需要安装 [VirtualBox](https://www.virtualbox.org/wiki/Downloads)。另外就是需要下载 Home Assistant 的[镜像文件](https://github.com/home-assistant/operating-system/releases/download/12.4/haos_ova-12.4.vdi.zip)。对于虚机，有一个推荐的配置，下面都以贴图的形式展现。

![系统](https://s2.loli.net/2024/06/30/iRuLXQxb56kJPzI.png)

![配置信息](https://s2.loli.net/2024/06/30/eRIdwYPNWmXH2aU.png)

这个步骤里面的虚拟硬盘，记得需要使用前面下载下来的 vdi 文件。

![虚拟硬盘](https://s2.loli.net/2024/06/30/kwIVFbTZmCzlqxH.png)

接着需要把虚机的网络里面去配置桥接，官方文档里面说必须要使用有线连接网络，但是我的笔记本使用 WIFI 也没有什么问题。

![image.png](https://s2.loli.net/2024/06/30/mVqNXzxMaUrcY9s.png)

系统全都配置好了之后，就直接启动系统，等待系统初始化好后即可。系统初始化好后，即可进入页面 http://homeassistant.local:8123/ 。一般进入页面的时候可能还需要等待一段时间初始化。

![welcome](https://s2.loli.net/2024/06/30/x2ovPRMyUTqsI18.png)

初始化完成后，创建账户。

![create-user.png](https://s2.loli.net/2024/06/30/Y7O3DGTN2cPsrmt.png)

选择家庭地址

![home-location.png](https://s2.loli.net/2024/06/30/7OmAfFaQVrBGyPq.png)

进入主页

![home-page.png](https://s2.loli.net/2024/06/30/zgn7QPflJA4FN3X.png)

以上就是 Home Assistant 的安装，主要就是一个虚机的配置，其它基本只要下一步就可以。不过这个还是只是第一步，还需要安装 HACS，它是一个插件商店，通过这个商店才可以去安装小米的插件。

## HACS 安装

HACS 需要尝试通过终端去安装，我尝试过直接在虚机里面去直接执行命令，但是是不可以的。需要安装终端插件去执行命令，这里我推荐使用 Terminal & SSH 插件，比另外一款插件好用，另外一款插件总是初始化失败。在设置里面，找到 Add-ons，然后在 ADD-ON 商店里面去搜索，不过这里有一个坑是默认搜不到这个插件的，需要在设置里面把高级模式打开。

![advanced-mode.png](https://s2.loli.net/2024/06/30/XO3NWnDoaB4LKCF.png)

![terminal.png](https://s2.loli.net/2024/06/30/HsdhwSjvabrz5WA.png)

![terminal-start.png](https://s2.loli.net/2024/06/30/HlDOT32BIinN4MU.png)

插件安装好了，可以参考[官方文档](https://hacs.xyz/docs/setup/download/)去安装 HACS。按照 Terminal 插件之后就可以直接执行命令：

```
wget -O - https://get.hacs.xyz | bash -
```

安装完毕后，需要重启一下 Home Assistant，可以直接在终端里面通过 `reboot` 来进行重启。安装重启之后，还需要在 Settings > Devices and Services > Add Integration > HACS 里面添加一下。因为 HACS 需要使用 github 去更新，你可能还需要一个 github 账号来进行配置，输入验证码后，即配置成功。

![GITHUB.png](https://s2.loli.net/2024/06/30/mNkUfxMon7YHJTe.png)

到这里，HACS 的安装就大功告成了。

![HACS.png](https://s2.loli.net/2024/06/30/vCflb8aIqe7Dp4J.png)

## 小米插件安装

通过 [hass-xiaomi-miot](https://github.com/al-one/hass-xiaomi-miot) 可以小米的插件，插件文档可以参考[这一篇](https://mp.weixin.qq.com/s/1y_EV6xcg17r743aV-2eRw)。这个文档里面是之前的老版本的界面，新版的界面已经发生变化了。小米插件安装成功后，也需要重启一下机器。安装完成之后继续选择 xiaomi 集成开始安装，需要通过小米账号来进行集成。小米账号可以支持小米的数字 ID 以及邮箱，就是你的小米账号。

![xiao-integration.png](https://s2.loli.net/2024/06/30/A4COpBN72KjkUr6.png)

![.png](https://s2.loli.net/2024/06/30/AVQJ65bxtwedWUT.png)

![xiaomi-login.png](https://s2.loli.net/2024/06/30/6isjUgpFb3v4uBR.png)

![exclude.png](https://s2.loli.net/2024/06/30/YwucRKIGJsNDVAT.png)

![overview.png](https://s2.loli.net/2024/06/30/j7yxYeV48SMNfWb.png)

## 门铃存储方案

在小米插件安装成功后，可以实现门铃视频的保存方案。创建一个文件 `xiaomi_video_autosave.sh`，可以通过 Terminal 插件，在 `/config` 目录下 创建这个文件。

```
cd /config
vi xiaomi_video_autosave.sh
```

```
#! /bin/bash
## setting section
path="/Volumes/sdb1/xiaomi/"
video_limit=50000

if [ ! -d $path ];then
  mkdir $path
fi

current_file_size=`ls $path|wc -l` 
video_url=$1
raw_file_name=`echo $2|sed 's/[^0-9]//g'` 
file_name=$path$raw_file_name".mp4"

if [ $current_file_size -ge $video_limit ]; then
  ls $path -tr|head -n $(($current_file_size-$video_limit+1))|sed "s/^/${path//\//\\\/}/g"|xargs rm
fi

ffmpeg -i $video_url -acodec copy -vcodec copy -f mp4 $file_name
```

path：就是存放目录，根据情况修改，格式为/media/xxxxxx/，不要省略结尾的“/”。可以在NAS或其他设备上存储，通过NFS挂载到/media下，见step4
video_limit：是存储上限，我存的视频大概不到1M一个，可以根据实际情况调整。

另外记得给脚本添加好执行权限。

```
chmod a+x xiaomi_video_autosave.sh
```

```
shell_command:
  xiaomi_autosave: '/bin/bash /config/xiaomi_video_autosave.sh "{{state_attr("camera.madv_mi3iot_c88d_video_doorbell","stream_address")}}" "{{state_attr("camera.madv_mi3iot_c88d_video_doorbell","motion_video_time")}}" ' 

##注意将以上两个camera实体换成你自己的！
```

接着是自动化流程的配置，可以放在 `automation.yaml` 中。

```
- id: '1678104080023'
  alias: door_video_autosave
  description: ''
  trigger:
  - platform: state
    entity_id:
    - camera.madv_mi3iot_c88d_video_doorbell  
    attribute: motion_video_time
  condition: []
  action:
  - service: shell_command.xiaomi_autosave
    data: {}
```

最终重启之后，尝试了终于保存视频成功了。

## 遗留问题

虽然折腾这么一大圈，总算能保存视频了，但是还是有两个遗留问题：

* 我想把视频放在 samba 共享里面，但是目前没有办法挂载上去
* 我访问 Home Assistant 的时候，经常会丢失连接，即丢失 homeassistant.local 的 DNS 解析，这个目前不知道是什么情况。



## Refrence

* https://github.com/al-one/hass-xiaomi-miot/issues/100#issuecomment-903078604
* https://bbs.hassbian.com/thread-20022-1-1.html
* https://medium.com/%E5%BD%BC%E5%BE%97%E6%BD%98%E7%9A%84-swift-ios-app-%E9%96%8B%E7%99%BC%E6%95%99%E5%AE%A4/%E5%AD%B8%E7%BF%92%E6%97%A5%E8%AA%8C-%E5%8D%81%E4%B9%9D-home-assistant%E4%BD%BF%E7%94%A8ssh-ad7c5dda5018