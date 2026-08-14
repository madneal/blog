---
title: "在 PythonAnywhere 部署第一个 Django 应用"
author: Neal
summary: "从 Git 拉代码、建虚拟环境、配置 WSGI 到访问域名，梳理在 PythonAnywhere 上部署 Django 的基本步骤与注意点。"
cover: "/img/post-covers/pythonanywhere-deploy-b513adb9a4.jpg"
tags: [Python, Django, 部署]
categories: [后端]
date: "2016-01-01"
lastmod: "2026-08-08"
---

## 为什么用 PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com/) 提供浏览器里的 Python 环境与 Web app 托管，适合练手部署 Django/Flask，免去自己买 VPS 配 Nginx 的门槛。免费层有限制，但够跑 demo。

## 步骤概览

1. 注册账号并打开 **Bash** 控制台  
2. 从 Git 拉取项目  
3. 创建并启用 virtualenv，安装依赖  
4. 在 Web 面板指定虚拟环境路径  
5. 编辑 **WSGI 文件** 指向 Django `application`  
6. Reload，用 `https://<user>.pythonanywhere.com` 访问  

## 拉代码与虚拟环境

```bash
git clone https://github.com/you/your-project.git
cd your-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Django 项目按需 migrate、collectstatic
```

Web 面板里 **Virtualenv** 填类似：

```text
/home/<your-username>/your-project/venv
```

## WSGI 配置示意

```python
import os
import sys

path = '/home/<your-username>/your-project'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

旧文使用 `whitenoise` 服务静态文件在部分教程里常见；Django 4+ 与 WhiteNoise 配置请以当前文档为准。生产务必设置 `ALLOWED_HOSTS`、关闭 `DEBUG`。

## 常见问题

| 问题 | 处理 |
|------|------|
| 500 | 看 Web 面板 error log |
| 静态 404 | `collectstatic` + WhiteNoise 或平台静态映射 |
| 依赖缺失 | 确认 Web 用的 venv 与 bash 里安装的是同一个 |
| 路径写错 | username、项目目录必须是绝对路径 |

## 小结

PythonAnywhere 把「能跑起来」变简单：核心是 **venv 路径正确 + WSGI 指到 application + ALLOWED_HOSTS**。这套步骤对理解后续更复杂的容器部署也有帮助。


## 适合与不适合

**适合：** 课程作业、个人 demo、低流量原型。  
**不适合：** 强 CPU 任务、长期高流量、需要任意系统包的特殊依赖（免费层限制多）。

把第一次部署走通后，再迁移到 Railway、Fly.io、容器 + 云主机时，你会发现概念一一对应：进程入口、环境变量、静态资源、域名与 HTTPS。PythonAnywhere 是很好的「部署第一课」。
