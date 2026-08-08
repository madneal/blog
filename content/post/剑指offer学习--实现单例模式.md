---
title: "剑指 Offer：C# 实现单例模式"
author: Neal
summary: "双重检查锁、静态构造函数、嵌套类延迟初始化三种 C# 单例写法，说明线程安全与懒加载差异，并修正旧文笔误。"
tags: [算法, C#, 设计模式]
categories: [设计模式]
date: "2015-11-13"
lastmod: "2026-08-08"
---

## 目标

保证一个类在进程内 **只有一个实例**，并提供全局访问点。面试与桌面端缓存/日志里常见。

## 1. 双重检查锁（懒加载）

```csharp
public sealed class Singleton
{
    private static readonly object SyncObj = new object();
    private static Singleton _instance;

    private Singleton() { }

    public static Singleton Instance
    {
        get
        {
            if (_instance == null)
            {
                lock (SyncObj)
                {
                    if (_instance == null)
                        _instance = new Singleton();
                }
            }
            return _instance;
        }
    }
}
```

外层判断避免每次都加锁；内层判断防止多线程重复创建。

## 2. 静态字段 + 运行时保证

```csharp
public sealed class Singleton
{
    private static readonly Singleton InstanceField = new Singleton();
    private Singleton() { }
    public static Singleton Instance => InstanceField;
}
```

.NET 保证类型初始化线程安全；实例在类型首次使用时创建，不一定等于首次访问 `Instance` 属性的时刻（取决于是否触碰了类型其它成员）。

## 3. 嵌套类延迟初始化

```csharp
public sealed class Singleton
{
    private Singleton() { }
    public static Singleton Instance => Nested.Instance;

    private class Nested
    {
        internal static readonly Singleton Instance = new Singleton();
        static Nested() { }
    }
}
```

只有真正用到 `Instance` 时才初始化嵌套类型，懒加载更干净。

## 现代 C#

也可使用 `Lazy<T>`：

```csharp
private static readonly Lazy<Singleton> Lazy =
    new(() => new Singleton());
public static Singleton Instance => Lazy.Value;
```

## 注意

- `sealed` 防止派生破坏单例  
- 多 AppDomain / 分布式不等于进程内单例  
- 旧文 `locak`/`Singelton`/`seled` 均为拼写错误  

## 小结

要线程安全懒加载：双重检查、`Lazy<T>` 或嵌套类；要简单：静态只读字段。先说清「是否懒加载 + 是否线程安全」，再写代码。


## 面试怎么讲

1. 先定义：唯一实例 + 全局访问  
2. 再说线程安全与懒加载是否需要  
3. 给出一种实现并分析  
4. 主动提：测试困难、隐藏依赖，现代更爱依赖注入  

能讲清 trade-off，比默写三种模板更加分。
