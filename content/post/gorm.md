
---
title: "AI 审代码，靠谱吗？"
author: Neal
tags: [安全, GORM, Go, AI]
categories: [安全]
date: "2025-08-22" 
---

### 背景：一道出乎意料的笔试题

最近在校招面试中，我发现一道关于 GORM SQL 注入的笔试题，所有人的答案都错了。题目代码大致如下：

```go
func UsersHandler(c *gin.Context) {
	groupId := c.Query("group_id")

	var group GroupModel
	// 注意这里的用法
	err := DB.First(&group, groupId).Error 
	if err != nil {
		c.Status(404)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"group": group,
	})
}
```

问题是：**这段代码是否存在 SQL 注入漏洞？**

正确答案是：**会**。

说实话，这个答案起初也让我感到意外。在日常业务开发中，我们很少会这样直接将变量传给 `First` 函数。`First` 通常用于获取按主键排序的第一条记录，更常见的做法是通过 `Where` 方法来构建查询条件。这不禁让我怀疑：这道题本身是不是有问题？

### 初探源码：`First` 函数的内部实现

简单看了一下 `First` 函数的实现：

```go
// First finds the first record ordered by primary key, matching given conditions conds
func (db *DB) First(dest interface{}, conds ...interface{}) (tx *DB) {
	tx = db.Limit(1).Order(clause.OrderByColumn{
		Column: clause.Column{Table: clause.CurrentTable, Name: clause.PrimaryKey},
	})
	if len(conds) > 0 {
		if exprs := tx.Statement.BuildCondition(conds[0], conds[1:]...); len(exprs) > 0 {
			tx.Statement.AddClause(clause.Where{Exprs: exprs})
		}
	}
	tx.Statement.RaiseErrorOnNotFound = true
	tx.Statement.Dest = dest
	return tx.callbacks.Query().Execute(tx)
}
```

从源码看，当 `conds` 参数不为空时，GORM 会调用 `tx.Statement.BuildCondition`来处理查询条件。

![image.png](https://i.postimg.cc/BbwDM7wZ/image.png)

乍看之下，`BuildCondition` 似乎会对传入的条件进行某种安全处理。但事实果真如此吗？

### AI 怎么说？

先将同样的问题抛给了市面上主流的大语言模型：

```
// 提问内容
func UsersHandler(c *gin.Context) {
	groupId := c.Query("group_id")

	var group GroupModel
	err := DB.Debug().First(&group, groupId).Error
	if err != nil {
		c.Status(404)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"group": group,
	})
}
上述的 First 函数是否会导致 sql 注入漏洞，请说明理由，理由简短，控制在100字符内。
```

结果出奇地一致，所有模型的回答都是“**不会**”导致 SQL 注入，理由也大同小异，都认为是 GORM 的参数化查询机制避免了风险。

![Sonnet 4](https://i.postimg.cc/76n4SfZw/image.png)

![GPT 5](https://i.postimg.cc/fTqkFgjm/image.png)

![Gemini](https://i.postimg.cc/zGfKHgpS/image.png)

![Claude](https://i.postimg.cc/ZKRck23L/image.png)

所有 AI 都给出了否定的答案。

### 动手验证

手动调试一下是最直观的，我创建了一个[简单的复现项目](https://github.com/madneal/codehub/tree/master/gorm_first)，使用 Docker 搭建数据库并运行示例应用。

接下来，我构造了一个经典的注入Payload，并发送请求：

`http://localhost:8080/users?group_id=1=1`

在 Goland 中，我在 `BuildCondition` 函数内部设置了断点。

![BuildCondition断点调试](https://i.postimg.cc/dVBYTM7y/image.png)

调试过程清晰地揭示了问题的根源：

当 `group_id` (`1=1`) 这个字符串传入时，GORM 首先会尝试将其转换为数字。当转换失败，且没有额外的 `args` 参数时，这个**字符串变量会被直接拼接到 `clause.Expr` 结构的 `SQL` 字段中**，最终作为原始 SQL 片段执行。

最终执行语句：

```sql
[10.482ms] [rows:1] SELECT * FROM `group_models` WHERE 1=1 ORDER BY `group_models`.`id` LIMIT 1
```

毫无疑问，这是一个 SQL 注入漏洞。

### 社区讨论与官方文档

经过进一步搜索，这其实并非一个新问题。早在几年前，就有人在 GORM 的 GitHub 上提过类似的 [Issue](https://github.com/go-gorm/gorm/issues/2517)。

![GORM Issue 截图](https://i.postimg.cc/SsKtRs3n/image.png)

社区对此的看法不一。有人认为这是框架的缺陷，但也有人认为，框架只是提供了执行原生 SQL 的能力，开发者有责任安全、合理地使用 ORM。

GORM 的作者也在官方安全[文档](https://gorm.io/docs/security.html)中明确指出了存在注入风险的用法，特别是“内联条件”（Inline Condition）查询。

![GORM安全文档截图](https://i.postimg.cc/1tqPXJLn/image.png)

实际上，GORM 的设计哲学是：**任何可以直接或间接传递 SQL 片段的函数，如果没有严格使用占位符（`?`）和参数绑定的方式，理论上都存在 SQL 注入的风险。**

### 结论

至此，真相大白。面试题的答案是正确的。这次小小的探索过程也给了我几点启示：

1.  **权威不容尽信**：无论是自己“想当然”的经验，还是 AI 模型看似专业的回答，都有可能出错。
2.  **动手验证至关重要**：面对疑问，尤其是涉及安全和底层原理的问题，没有什么比亲手调试和验证更可靠。
3.  **理解工具而非滥用**：ORM 框架极大地提升了开发效率，但前提是我们必须理解其工作原理和安全边界，而不是将其当作一个永不出错的黑盒。

所以，AI 审代码，现阶段真的靠谱吗？或许它可以作为辅助，但绝不能替代开发者自身的深度思考和验证。

还有，这篇文章是不是 AI 味也挺重的😄

