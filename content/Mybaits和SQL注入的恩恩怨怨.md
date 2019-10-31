---
title: "Mybatis 和 SQL 注入的恩恩怨怨"
author: Neal
tags: [安全, web 安全, SQL 注入]
categories: [安全]
date: "2019-10-30" 
---

Mybatis 是一种持久层框架，介于 JDBC 和 Hibernate 之间。通过 Mybatis 减少了手写 SQL 语句的痛苦，使用者可以灵活使用 SQL 语句，支持高级映射。但是 Mybatis 的推出不是只是为了安全问题，有很多开发认为使用了 Mybatis 就不会存在 SQL 注入了，真的是这样吗？使用了 Mybatis 就不会有 SQL 注入了吗？答案很明显是 NO。 Mybatis 它只是一种持久层框架，它并不会为你解决安全问题。当然，如果你能够遵循规范，按照框架推荐的方法开发，自然也就避免 SQL 注入问题了。本文就将 Mybatis 和 SQL 注入这些恩恩怨怨掰扯掰扯。

## 起源

写本文的起源主要是来源于内网发现的一次 SQL 注入。我们发现内网的一个请求的 keyword 参数存在 SQL 注入，简单地介绍一下需求背景。基本上这个借口就是实现多个字段可以实现 keyword 的模糊查询，这应该是一个比较常见的需求。只不过这里存在多个查询条件。经过一番搜索，我们发现问题的核心处于以下代码：

```java
public Criteria addKeywordTo(String keyword) {
  StringBuilder sb = new StringBuilder();
  sb.append("(display_name like '%" + keyword + "%' or ");
  sb.append("org like '" + keyword + "%' or ");
  sb.append("status like '%" + keyword + "%' or ");
  sb.append("id like '" + keyword + "%') ");
  addCriterion(sb.toString());
  return (Criteria) this;
}
```

很明显，需求是希望实现 `diaplay_name`, `org`, `status` 以及 `id` 的模糊查询，但开发在这里自己创建了一个 `addKeywordTo` 方法，通过这个方法创建了一个涉及多个字段的模糊查询条件。我们在内网发现的绝大多数 SQL 注入的注入点基本都是模糊查询的地方。可能很多开发往往觉得模糊查询是不是就不会存在 SQL 注入的问题。分析一下这个开发为什么会这么写，在他没有意识到这样的写法存在 SQL 注入问题的时候，这样的写法肯定是最省事的，到时直接把查询条件拼进去就可以了。以上代码是问题的核心，我们再看一下对应的 xml 文件：

```xml
  <sql id="Example_Where_Clause" >
    <where >
      <foreach collection="oredCriteria" item="criteria" separator="or" >
        <if test="criteria.valid" >
          <trim prefix="(" suffix=")" prefixOverrides="and" >
            <foreach collection="criteria.criteria" item="criterion" >
              <choose >
                <when test="criterion.noValue" >
                  and ${criterion.condition}
                </when>
                <when test="criterion.singleValue" >
                  and ${criterion.condition} #{criterion.value}
                </when>
                <when test="criterion.betweenValue" >
                  and ${criterion.condition} #{criterion.value} and #{criterion.secondValue}
                </when>
                <when test="criterion.listValue" >
                  and ${criterion.condition}
                  <foreach collection="criterion.value" item="listItem" open="(" close=")" separator="," >
                    #{listItem}
                  </foreach>
                </when>
              </choose>
            </foreach>
          </trim>
        </if>
      </foreach>
    </where>
  </sql>

    <select id="selectByExample" resultMap="BaseResultMap" parameterType="com.doctor.mybatisdemo.domain.userExample" >
    select
    <if test="distinct" >
      distinct
    </if>
    <include refid="Base_Column_List" />
    from user
    <if test="_parameter != null" >
      <include refid="Example_Where_Clause" />
    </if>
    <if test="orderByClause != null" >
      order by ${orderByClause}
    </if>
  </select>
```

我们再回过头看一下上面 JAVA 代码中的 `addCriterion` 方法，这个方法是通过 Mybatis generator 生成的。

```java
protected void addCriterion(String condition) {
    if (condition == null) {
        throw new RuntimeException("Value for condition cannot be null");
    }
    criteria.add(new Criterion(condition));
}
```

这里的 `addCriterion` 方法只传入了一个字符串参数，这里其实使用了重载，还有其它的 `addCriterion` 方法传入的参数个数不同。这里使用的方法只传入了一个参数，被理解为 `condition`，因此只是添加了一个只有 `condition` 的 Criterion。现在再来看 xml 中的 `Example_Where_Clause`，在遍历 criteria 时，由于 criterion 只有 condition 没有 value,那么只会进去条件 `criterion.noValue`，这样整个 SQL 注入的形成就很清晰了。

```xml
<when test="criterion.noValue" >
    and ${criterion.condition}
</when>
```

### 正确写法

既然上面的写法不正确，那正确的写法应该是什么呢？第一种，我们可以用一种非常简单直接的方法，在 `addKeywordTo` 方法里面 对 keword 进行过滤，这样其实也可以避免 SQL 注入。通过正则匹配将 keyword 里面所有非字母或者数字的字符都替换成空字符串，这样自然也就不可能存在 SQL 注入了。

```java
keyword = keyword.replaceAll("[^a-zA-Z0-9\\s+]", "");
```

但是这种写法并不是一种科学的写法，这样的写法存在一种弊端，就是如果你的 keyword 需要包含符号该怎么办，那么你是不是就要考虑更多的情况，是不是就需要添加更多的逻辑判断，是不是就存在被绕过的可能了？