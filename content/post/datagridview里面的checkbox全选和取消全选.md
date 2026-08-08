---
draft: true
title: "WinForms DataGridView：CheckBox 列的全选与取消全选"
author: "Neal"
summary: "遍历 DataGridView 勾选列实现全选/取消全选，并补充布尔值写入方式、表头全选、大数据量与数据绑定注意点。"
tags: [C#, WinForms, .NET]
categories: [winform开发]
date: "2015-04-22"
lastmod: "2026-08-08"
---


桌面管理系统里，表格第一列放 CheckBox、工具栏放「全选 / 取消全选」非常常见。逻辑不复杂，但 `DataGridView` 的单元格值类型、编辑提交时机，经常让人写出「点了没反应」的代码。

## 基本实现

假设第 0 列是 `DataGridViewCheckBoxColumn`：

```csharp
private void selectAll_Click(object sender, EventArgs e)
{
    for (int i = 0; i < dataGridView1.Rows.Count; i++)
    {
        var row = dataGridView1.Rows[i];
        if (row.IsNewRow) continue; // 允许用户添加行时跳过最后空行

        bool selected = false;
        if (row.Cells[0].Value != null && row.Cells[0].Value != DBNull.Value)
            selected = Convert.ToBoolean(row.Cells[0].Value);

        if (!selected)
            row.Cells[0].Value = true; // 用 bool，而不是字符串 "True"
    }
    dataGridView1.EndEdit();
}

private void cancelAll_Click(object sender, EventArgs e)
{
    for (int i = 0; i < dataGridView1.Rows.Count; i++)
    {
        var row = dataGridView1.Rows[i];
        if (row.IsNewRow) continue;
        row.Cells[0].Value = false;
    }
    dataGridView1.EndEdit();
}
```

## 为什么不建议写 `"True"` / `"False"` 字符串

CheckBox 列底层期望的是 **布尔** 或可转换的值。写入字符串有时能显示，但在：

- 数据绑定到 `bool` 属性  
- 参与条件过滤  
- 与三态（Indeterminate）交互  

时容易出现类型不一致。统一用 `true` / `false`。

## 表头复选框（更现代的 UX）

比两个按钮更省地方的做法是：在列头画一个 CheckBox，点击切换全部状态。实现要点：

1. 处理 `ColumnHeaderMouseClick`  
2. 维护 `_allChecked` 状态  
3. 批量赋值后 `InvalidateHeader` 重绘  

若行数上万，循环赋值会卡 UI，可：

- 临时 `dataGridView1.SuspendLayout()`  
- 或在绑定的 `DataTable` / `BindingList` 层改数据，再一次性重置绑定  

## 数据绑定场景

若网格绑的是对象列表：

```csharp
public class RowItem { public bool Checked { get; set; } public string Name { get; set; } }
```

应改 `Checked` 属性并通知 `INotifyPropertyChanged`，而不是只改单元格 `Value`，否则保存时丢状态。

## 权限与安全（桌面程序也有）

全选后批量删除、批量导出时：

- 二次确认  
- 记录操作者与数量  
- 对敏感列（路径、密钥）导出前脱敏  

这些和 Web 后台的 bulk action 是同一类风险。

## 小结

| 点 | 建议 |
|----|------|
| 赋值类型 | `true`/`false` |
| 新行 | 跳过 `IsNewRow` |
| 编辑态 | `EndEdit()` |
| 大数据 | 暂停布局或改数据源 |
| UX | 表头 CheckBox 优于双按钮 |

把全选做对，本质是：**改对数据模型，而不是只改屏幕上的方框**。
