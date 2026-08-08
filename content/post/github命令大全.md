---
draft: true
title: "Git 常用命令速查（从配置到协作）"
author: Neal
summary: "按场景整理 Git 常用命令：配置、提交、分支、暂存、历史与撤销。纠正「GitHub=Git」的说法，便于日常检索。"
tags: [Git, 开发工具]
categories: [开发工具]
date: "2015-10-25"
lastmod: "2026-08-08"
---

> 说明：标题沿用旧文，但正文区分 **Git**（版本控制系统）与 **GitHub**（托管平台）。下列为命令行 Git。

## 配置

```bash
git config --global user.name "yourname"
git config --global user.email "you@example.com"
git config --global core.editor "vim"
git config --list
```

## 创建与克隆

```bash
git init
git clone <url>
git clone <url> <dir>
```

## 日常提交

```bash
git status
git diff                 # 工作区 vs 暂存区
git diff --staged        # 暂存区 vs HEAD
git add <file>
git add -p               # 交互暂存
git reset HEAD <file>    # 取消暂存，保留修改
git commit -m "msg"
git commit --amend       # 改最后一次提交（未推送时）
```

## 分支

```bash
git branch
git branch <name>
git switch <name>        # 或 git checkout <name>
git switch -c <name>
git merge <branch>
git branch -d <name>
```

## 远程

```bash
git remote -v
git fetch
git pull
git push -u origin HEAD
```

## 暂存现场

```bash
git stash push -m "wip"
git stash list
git stash pop
git stash drop
```

## 历史

```bash
git log --oneline --graph -20
git log --follow -- <file>
git show <commit>
```

## 撤销（慎用）

```bash
git restore <file>           # 丢弃工作区修改
git revert <commit>          # 新提交抵消
git reset --soft <commit>    # 回退提交，保留暂存
git reset --hard <commit>    # 危险：丢本地未推送工作
```

## .gitignore 示例

```gitignore
*.log
build/
node_modules/
.DS_Store
```

## 小结

先建立 **工作区 / 暂存区 / 提交 / 远程** 四层模型，再记命令会快很多。需要桌面客户端可用 GitHub Desktop 等，但原理仍是这套 Git 对象模型。


## 推荐日常工作流

1. 从 `main`/`master` 拉最新：`git switch main && git pull`  
2. 开功能分支：`git switch -c feature/x`  
3. 小步提交，信息写清「为什么」  
4. 推远程并发 PR，避免直接推受保护分支  
5. 评审合并后删除已合并分支  

## 易混概念

| 概念 | 含义 |
|------|------|
| 工作区 | 你正在改的文件 |
| 暂存区 | `git add` 后等待 commit 的快照 |
| HEAD | 当前提交指针 |
| origin | 默认远程名，不是特殊协议 |

把命令当「改这四层状态的工具」，比死记参数快。需要撤销时先问：改动是否已推送？未推送可用 reset；已推送优先 revert。


## 远程协作最小集

本地提交只存在于你的磁盘；`git push` 之后同事才能 `fetch`/`pull` 到。冲突发生在合并双方都改了同一区域时：打开文件找冲突标记，手动保留正确版本，再 `add` + `commit` 完成合并。

若误把密钥、大文件提交进历史，应立刻轮换密钥，并使用 `git filter-repo` 等工具清理历史（超出本文范围，但务必知道「删文件再 commit 一次」不够）。

命令速查解决的是「语法」；协作规范（分支命名、PR 模板、保护主分支）解决的是「团队怎么不乱」。两者都要。
