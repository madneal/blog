---
title: "cve check"
author: Neal
summary: "本文围绕《cve check》梳理安全开发、安全、漏洞分析和Python相关的背景、方法和实践细节，可作为排查与学习记录。"
cover: "/img/post-covers/check-cve-de56a112ab.jpg"
tags: [安全, 漏洞分析, Python]
categories: [安全开发]
date: "2019-07-04"
lastmod: "2026-08-08"
---

今天想检查一下 Gitlab 11.9.0 产品受哪些 cve 的影响。其实网上已经有很多网站可以查询产品的相关 cve，但就是粒度比较粗。我想在 cve 列表中筛选出特定的版本，已经特定的版本，比如是社区版还是旗舰版。找了一下，没有发现完全符合这个要求的。后来在网上我就看到了一个网站是可以提供 cve 的 API 查询的。可以通过网站 API 可以获取特定的数据。

可以通过 https://cve.circl.lu/api/ 可以看到 API 文档。可以通过 cve id 以及 product 以及其他更多信息来查询。最有用的 API 就是这一个，



> **（原外链配图已失效移除，请以正文说明为准）**



可以通过 vendor 以及 product 获取指定 vendor 和 product 的 cve 列表。这个 API 返回的结果是一个 JSON 数组，我们需要在这里面过滤出相应的版本号以及 edition 版本。另外由于请求的结果一般是一个很长的 json 数据，我的做法是第一次请求，可以吧结果保存成 JSON 文件，第二次请求的时候首先检查这个 JSON 文件的最近修改时间，如果最近修改时间小于指定的天数，比如 3 天，如果 3 天内修改过的话，直接从 JSON 文件加载数据，否则重新发送请求，加载数据。

```
# check if file modified in the last several days
def check_file_modified(filename, days):
    file_modify_time = getmtime(filename)
    return time() - file_modify_time < (days * 3600 * 1000)


def write_json(filename, result):
    with open(filename, 'w') as f:
        dump(result, f, indent=2)


def write_csv(filename, result, header):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for ele in result:
            writer.writerow([ele["id"], ele["last-modified"], ele["cvss"], ele["summary"]])


def search(params, options):
    url = "https://cve.circl.lu/api/search/" + params
    print(url)
    filename = f"{params.replace('/', '-')}.json"
    try:
        if isfile(filename) and check_file_modified(filename, 3):
            with open(filename, 'r') as f:
                result = loads(f.read())
        else:
            res = get(url)
            if res.status_code == 200:
                with open(filename, 'w') as f:
                    f.write(res.text)
                result = loads(res.text)
            else:
                print("Request failed: %d".format(res.status_code))
        cve_result = []
        for ele in result:
            if has_cve(ele, options.vendor, options.product, options.version, options.edition):
                obj = {
                    "id": ele["id"],
                    "last-modified": ele["last-modified"],
                    "cvss": ele["cvss"],
                    "summary": ele["summary"]
                }
                cve_result.append(obj)
            else:
                continue
        print(f"{options.vendor}:{options.product}:{options.version}:{options.edition} "
              f"has impacted by {len(cve_result)} cve")
        if options.output is None or options.output == "csv":
            write_csv("result.csv", cve_result, ["id", "last-modified", "cvss", "summary"])
        else:
            write_json("result.json", cve_result)
    except Exception as e:
        print(e)
```

完整的项目地址可以参考 https://github.com/neal1991/check-cve/blob/master/check-cve.py


## 用 CIRCL CVE API 做版本筛选的思路

公开站点粒度粗时，可走 [cve.circl.lu API](https://cve.circl.lu/api/) 拉产品相关条目，再在本地按版本区间过滤（社区版/企业版关键字、cpe 字符串）。

典型流程：

1. 按 vendor/product 拉取候选 CVE 列表  
2. 解析 description / vulnerable_configuration 中的版本线索  
3. 与资产台账中的精确版本比对  
4. 输出「影响 / 不影响 / 需人工确认」三态  

注意：公开 API 的 CPE 与版本语法并不完美，**不能替代原厂 advisory**，只能做初筛。

## 企业内更稳的做法

- 订阅 NVD/OSV/GitHub Advisory，结合 SBOM  
- 用 `grype` / `trivy` 扫容器与文件系统  
- 维护内部「产品-版本-补丁」矩阵  
- 高危洞 24h 内人工确认利用前提（需认证？默认配置？）

## 小结

「查 CVE」不是打开一个网页，而是 **数据源 + 版本语义 + 资产上下文**。API 帮你自动化初筛，最终结论仍要落到补丁与风险接受记录上。


## 输出给业务方的格式

| 字段 | 说明 |
|------|------|
| CVE | 编号与链接 |
| 产品版本 | 资产实值 |
| 利用条件 | 网络/权限/配置 |
| 补丁版本 | 官方修复 |
| 临时缓解 | WAF/禁用功能 |
| 截止时间 | 按等级 |

表格化输出比丢一串链接更容易推动修复。


## 延伸阅读与实践

把文章里的命令和配置放到自己的实验环境跑一遍，比只看结论更重要。建议同步记录：环境版本、失败现象、最终生效的配置。下次遇到同类问题时，检索自己的笔记往往比搜引擎更快。

若该主题涉及安全测试，请仅在明确授权的系统或官方靶场中操作，并保留测试范围与时间窗记录，避免对生产造成误伤。

对团队分享时，用「问题—影响—修复—验证」四段结构复述，有助于把个人经验沉淀为组织能力。
