---
title: "Logstash技巧之处理不同的output"
author: Neal
summary: "Logstash 多输出时，如何用 clone 让 Kafka 与 ES 使用不同字段集：场景、配置思路、替代方案与注意点。"
cover: "/img/post-covers/logshsh-output-d17ae3fd1f.jpg"
tags: [工具, Logstash, ELK]
keywords: [插件, logstash, clone]
categories: [工具]
date: "2020-05-18"
lastmod: "2026-08-08"
---

## 场景

用 Logstash 时遇到一个小需求：

- **Output A → Kafka**：不希望带 `@timestamp`（或其它字段）  
- **Output B → Elasticsearch**：需要保留 `@timestamp`

在 **filter** 阶段用 `mutate { remove_field => ... }` 会作用在整条事件上，**所有 output 一起少字段**。我需要的是：**同一条日志，不同出口，字段集不同**。

## 思路：先 clone，再分别改

`clone` 过滤器可以把当前事件复制出一份（或多份），并打上 type/tags，之后在 filter 里按类型分支处理，最后在 output 用 `if` 分流。

概念流：

```text
input → filter(clone) → filter(对 clone 删字段) → output(if 原事件→ES, if clone→Kafka)
```

## 配置示意

```ruby
filter {
  # 复制一份，type 设为 kafka_copy（名称自定）
  clone {
    clones => ["kafka_copy"]
  }

  if [type] == "kafka_copy" {
    mutate {
      remove_field => ["@timestamp"]
      # 也可 remove 其它仅 ES 需要的字段
    }
  }
}

output {
  if [type] != "kafka_copy" {
    elasticsearch {
      hosts => ["http://es:9200"]
      index => "app-logs-%{+YYYY.MM.dd}"
    }
  }

  if [type] == "kafka_copy" {
    kafka {
      topic_id => "app-logs"
      codec => json
    }
  }
}
```

注意：

1. `clone` 之后原事件与副本都会继续走后续 filter，务必用 **条件** 包住删除逻辑。  
2. 字段名、`type`/`tags` 策略按你现有流水线习惯调整；有人用 `tags` 而不是 `type`。  
3. 版本差异：查阅你使用的 Logstash 版本文档确认 `clone` 插件是否默认可用。

## 其它做法

| 做法 | 说明 |
|------|------|
| 两条 pipeline | 清晰，但维护成本高 |
| 仅在 Kafka codec/处理器侧丢字段 | 取决于下游是否支持 |
| 在 ES 用 ingest pipeline | 适合「ES 多字段、Kafka 全量」的反场景 |
| 上游直接分叉（Filebeat 多 output） | 有时比 Logstash 更简单 |

## 坑

- **事件翻倍**：clone 后吞吐与 license/资源按两条计，量大时要评估。  
- **顺序与指纹**：副本是独立事件，幂等与去重逻辑要分开想。  
- **监控**：失败重试时确认两个 output 的死信策略。  

## 小结

多 output 要「同学不同貌」，优先 **clone + 条件 mutate + 条件 output**。这比在 output 插件里找「按目的地删字段」更通用，也是当时卡住很久后最省事的解法。


## 与 pipeline-to-pipeline 的对比

Logstash 多 pipeline + pipeline-to-pipeline 通信也能实现「分叉」，适合超大流量与隔离失败域。小团队单 pipeline + `clone` 通常足够，配置也集中。

## 观测与测试

- 用 `stdout { codec => rubydebug }` 临时验证 clone 后字段  
- 指标：events.in / events.out、Kafka 发送失败、ES reject  
- 变更配置走 `logstash --config.test_and_exit`

## 安全

日志可能含 token、身份证号。对 Kafka 与 ES 的字段集做不同脱敏时，clone 正好能「出口 A 打码、出口 B 全量仅限安全区」。别把全量敏感日志送到低权限主题。

## 小结

`clone` 解决的是 **同一事件多出口异构**。先分叉再 mutate，比在 output 里硬掰字段更清晰；量大时再评估双 pipeline。


## 配置片段放置建议

将 `clone` 相关 filter 单独放进片段文件，用 `config.reload.automatic` 或编排工具下发。评审时重点看：条件是否写反、是否误删两边都需要的字段、Kafka 与 ES 失败是否互相拖累。

复杂路由最终应画一张数据流图贴进仓库 README，新人才能快速理解「为什么有两条几乎一样的事件」。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
