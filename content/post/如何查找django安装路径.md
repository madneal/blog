---
draft: true
title: "如何查找 Django 的安装路径与版本信息"
author: "Neal"
summary: "用 django.__file__、pip show、python -c 等方式定位 Django 安装目录，并说明虚拟环境、多 Python 并存时的排查思路。"
tags: [Django, Python, 后端]
categories: [后端]
date: "2015-10-10"
lastmod: "2026-08-08"
---


调试模板标签、阅读源码、确认「到底 import 到了哪一份 Django」时，第一件事往往是：**安装路径在哪**。文档里有时写得很绕，其实 Python 自己就能告诉你。

## 最快的方式

在你 **实际运行项目的同一个解释器** 里执行：

```bash
python -c "import django; print(django.__file__); print(django.get_version())"
```

示例输出：

```text
/Users/you/.venv/lib/python3.12/site-packages/django/__init__.py
5.0.2
```

包根目录就是 `__file__` 所在目录的上一级（去掉 `__init__.py`）。

在 REPL 里也一样：

```python
import django
django  # 交互环境有时会显示 repr
print(django.__file__)
print(django.get_version())
```

## 用 pip 查看元数据

```bash
pip show django
# 或
python -m pip show django
```

关注：

- `Version`  
- `Location`（site-packages 路径）  
- `Requires`  

若 `pip show` 有结果但 `import django` 失败，多半是 **pip 绑定的 Python 与当前 shell 的 python 不是同一个**。

## 多环境并存时怎么排

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| 系统 Python 有 Django，venv 没有 | 没装进虚拟环境 | `python -m pip install django` |
| 版本与预期不符 | PATH 指错解释器 | `which python` / `py -0p` |
| IDE 能跑、终端不能跑 | IDE 选了别的 interpreter | 对齐解释器 |
| Docker 内路径不同 | 容器内 site-packages | 在容器里执行同上命令 |

永远记住：**路径必须相对于「运行 manage.py 的那个 python」**。

## 源码阅读小技巧

```bash
python -c "import django, pathlib; print(pathlib.Path(django.__file__).resolve().parent)"
```

然后用编辑器直接打开该目录，例如查 `django/middleware/`、`django/contrib/auth/`。

## 和安全相关的一点

生产镜像里请固定版本（`Django==x.y.z`），并关注 [Django security releases](https://www.djangoproject.com/weblog/)。「能 import」不等于「版本可接受」；查路径的同时把 `get_version()` 记进部署检查清单。

## 小结

1. `python -c "import django; print(django.__file__)"` 最直接  
2. `pip show django` 看安装元数据  
3. 路径争议 = 解释器争议，先统一 `python`  
4. 顺手打印版本，避免环境漂移  

这就是当年那条「`import django; django`」笔记真正想表达的东西——补全上下文后，它才配得上单独成文。
