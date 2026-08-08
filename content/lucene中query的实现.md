---
title: "lucene 中 query 的实现"
author: Neal
summary: "梳理 Lucene 常见 Query 类型与继承关系，并以 RegexpQuery 为入口说明 MultiTermQuery / AutomatonQuery 的职责边界。"
tags: [后端, Java, Lucene, 学习笔记]
categories: [java]
date: "2018-10-09"
lastmod: "2026-08-08"
---

## 背景

做搜索或读 Elasticsearch/Lucene 相关代码时，会不断碰到各种 `Query`。它们不是「SQL 的 where 语法糖」那么简单：每种 Query 对应不同的 **匹配语义** 与 **执行计划**（是否可走倒排、是否要自动机、是否要算分等）。

## 常见 Query 类型

Lucene 里常见的包括：

| 类型 | 大致用途 |
|------|----------|
| `TermQuery` | 精确 term |
| `BooleanQuery` | 多子句布尔组合 |
| `PhraseQuery` / `MultiPhraseQuery` | 短语、多短语 |
| `PrefixQuery` | 前缀 |
| `WildcardQuery` | 通配 |
| `FuzzyQuery` | 模糊（编辑距离） |
| `RegexpQuery` | 正则 |
| `TermRangeQuery` / `PointRangeQuery` | 词项/数值点范围 |
| `ConstantScoreQuery` | 固定分 |
| `DisjunctionMaxQuery` | 多查询取 max 分 |
| `MatchAllDocsQuery` | 全匹配 |

它们大都继承抽象类 `Query`，再按能力向上抽象出 `MultiTermQuery` 等中间层。可以组合使用，例如 Boolean 里嵌 Term + Phrase。

## 继承链：以 RegexpQuery 为例

`RegexpQuery` 的继承关系大致是：

```text
Query
  └── MultiTermQuery
        └── AutomatonQuery
              └── RegexpQuery
```

含义：

1. **Query**  
   抽象根：重写、访问权重、创建 `Weight`/`Scorer` 的模板。

2. **MultiTermQuery**  
   「一个字段上由多个 term 组成的匹配」。通配、前缀、正则、模糊都可能落到「先枚举 term 再合成」的路径。子类要实现如何从 term 字典枚举。

3. **AutomatonQuery**  
   用 **自动机（Automaton）** 描述可接受的 term 集合，在 term 字典上做高效求交/枚举。正则、部分通配会先编译成自动机。

4. **RegexpQuery**  
   把用户正则编译为自动机，再交给 `AutomatonQuery` 执行。

因此读 `RegexpQuery` 源码时，真正的「怎么搜」往往在父类的枚举与 `Weight` 构建里，子类更偏 **构造与正则→自动机**。

## 使用上的注意

- **性能**：前缀/正则/模糊可能扫描大量 term，生产要限制前导通配（`*foo`）和复杂正则。  
- **分析器**：Query 作用在 **索引后的 term** 上，不是原始句子；字段 analyzer 与 search analyzer 要一致理解。  
- **与 ES 的关系**：ES 的 query DSL 最终多会落到 Lucene Query；懂类型有助于解释「为什么这个查询慢」。  

## 建议的阅读顺序

1. `TermQuery` / `BooleanQuery`（主干）  
2. `MultiTermQuery` 的枚举接口  
3. `AutomatonQuery` + `RegexpQuery`  
4. 再看 `IndexSearcher` 如何建 `Weight`

## 小结

Lucene Query 体系是「语义 → 可执行结构」的分层。`RegexpQuery` 不是孤立类，而是 **正则 → 自动机 → 多 term 枚举 → 打分** 链路上的一环。抓住继承关系，源码阅读会顺很多。
