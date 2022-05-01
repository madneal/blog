---
title: "goland-2022.01版本最新实用功能"
author: Neal
tags: [goland,Go]
keywords: [goland,Go]
categories: [开发工具]
date: "2022-05-01" 
---

在 Go 的开发过程中，经常遇到一个非常麻烦的问题就是 `JSON` 的解析。因为 Go 中的 `JSON` 的解析，一般来说需要定义对应 `JSON` 的 struct。或者使用 `interface{}` 类型来进行定义，然后再进行类型的转换。当然这在 Python 中可能两三句话就搞定了。

在 Goland 2022.01 最新版本中，终于迎来了在 `JSON` 方面解析的便捷功能。在最新版本中，只要将 `JSON`  粘贴到 IDE 中就会提示是否转化为 `struct` 类型，所有的字段都会被生成，相对于以前的一个个的手动的定义要方便太多太多了。

![go_converting_json_to_struct.animated.gif](https://s2.loli.net/2022/05/01/vrSC83Kauqls1UY.gif)

还可以使用 Action 来进行转换动作，`Generate Go Type form JSON`：

![go_modify_json_for_a_struct_in_a_separate_dialog.animated.gif](https://s2.loli.net/2022/05/01/3vfFiJLTnHZ7h5q.gif)

同时还可以添加新的 tag，key 以及修改 key 的代码风格，调用来说一般使用 `alt+enter` 快捷键即可。

## Intention actions

字段添加新的 tag 

1. 点击 `struct` 的字段然后按 `alt+enter`
2. 选择 `Add key to tags`

![go_add_new_tags_to_a_struct_field.animated.gif](https://s2.loli.net/2022/05/01/GQ4BeAxFrzinKPw.gif)

修改 key

1. 点击 `struct` 的字段然后按 `alt+enter`
2. 选择 `Update key value in tags`

![go_modify_keys_in_field_tags.animated.gif](https://s2.loli.net/2022/05/01/fEBJmDLhl8KeoIa.gif)

修改 key 的代码风格

1. 点击 `struct` 的字段然后按 `alt+enter`
2. 选择 `Change field name style in tags`

![go_change_code_style_of_tag_keys.animated.gif](https://s2.loli.net/2022/05/01/vfxXRiu8U9QGN2h.gif)

## 代码补全

当修改 key 的时候，Goland 会展示最有可能的候选值。比如，`json` 会建议 `omitempty`，`xml` 会建议 `attr`，`cdata`，`chardata` 以及 `innerxml` 等。

## Reference

* https://www.jetbrains.com/help/go/working-with-json.html#intention-actions-json