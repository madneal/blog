---
draft: true
title: "SQLite 实用操作：CSV 导入、乱码、时区与 database is locked"
author: Neal
summary: "命令行导入 CSV、中文乱码、datetime 本地时间，以及 database is locked 的常见原因与关闭连接习惯。"
tags: [后端, SQLite, 数据库]
categories: [数据库]
date: "2015-04-15"
lastmod: "2026-08-08"
---

## 用命令行导入 CSV

免费版 GUI 可能没有 import 菜单，用 CLI 即可。CSV **列顺序与表结构一致**，通常先去掉表头或 `.import` 时注意 header 选项（视版本）。

```bash
sqlite3 my.db
```

```sql
.mode csv
.separator ','
.import data.csv my_table
```

也可用：

```bash
sqlite3 my.db ".mode csv" ".import data.csv my_table"
```

## 中文乱码

导入前把文件转为 **UTF-8**（记事本「另存为」或 `iconv`）。SQLite 内部以 UTF-8 为主，源文件编码不对就会花。

## datetime 时间不准

```sql
SELECT datetime('now');              -- UTC 语义常见
SELECT datetime('now', 'localtime'); -- 本地时区
```

应用层更推荐存 **UTC**，展示时再转本地。

## database is locked

常见原因：

1. 另一个连接未关闭（读未放、写事务未结束）  
2. 多进程同时写，默认锁粒度导致等待超时  
3. 异常路径忘记 `close`

习惯：

- `using` / `try/finally` 关闭 connection、reader  
- 长只读可考虑 WAL 模式（`PRAGMA journal_mode=WAL;`）  
- 控制事务范围，尽快 commit/rollback  

## 小结

SQLite 轻便，但 **编码、时区、连接生命周期** 三个细节最容易在业务里炸。命令行导入 + 严谨关闭连接，能解决大部分「小库大麻烦」。


## 和嵌入式场景

移动端、桌面端、边缘设备常用 SQLite。锁问题在「UI 线程写库 + 后台同步写库」时尤其明显，应用层应串行化写操作或上队列。

备份很简单：停写后复制单个 `.db` 文件（注意 WAL 模式下还有 `-wal`/`-shm`）。理解这些运维细节，比背更多 SQL 方言更有用。
