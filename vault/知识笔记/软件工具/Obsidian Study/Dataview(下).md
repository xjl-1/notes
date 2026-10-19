---
title: Dataview（下）
tags: [Obsidian, Dataview, 查询, 函数]
created: 2026-06-04
type: note
status: active
summary: Dataview 插件进阶：task/calendar 查询、数据类型、函数表达式、日期函数与实战示例。
---

* task
	* 任务属性
		* completed已完成
	* 分组 
	* group by completed/tags
* calender
	* 必须带有日期属性
	* 如 file.ctime

# 运算基础
## 数据类型
* number
	* 3
* string
	* 字符串
* date
	* 2024-01-01
* list
	* file.tags
* bool
	* true/false
* 相同的数据类型才可以运算
## 数据的运算方式(类比python)
* 数字运算(加减乘除)
* 比较
# 函数
## 什么是函数？
* 函数表达式
	* 元素 操作(参数)
* 一个比喻
	* 元素：猫(cat)
	* 函数：吃(eat),跳(jump)
	* 执行函数
		* cat.eat()
		* 吃什么？
		* cat.eat("fish")
		* 参数类型：字符串
		* cat.jump()
		* 跳多远？
		* cat.jump(50)
		* 参数类型：数字

## 举例
* contains()
* 一个元素是否包含另一个元素(前一个包含后一个)
	* `contains(string,string) =bool`
	* 参数类型：字符串
	* 返回值：bool
	* `dataview
	* list
	* where contains(file.tags,"Obsidian"）`
	* 以上类比寻找所有标签中有Obsidian的笔记

## 必须掌握

* 数据类型转换
	* 字符串转换成数字
		* number(string)
	* 数字转换成字符串
		* string(any)

# 日期函数

* 指定日期
	* date(2025-09-09)
* 获取当前日期
	* date(today)
* 获取当前日期时间
	* date(now)
* 获取时间跨度： dur()
	* dur(5m)
	* dur(3d)
	* 月:mo
	* 年:yr

> 最近七天修改的笔记

```dataview
table file.mday as "修改日期"
where file.mday >=date(today) - dur(7d)
```

* 注意dataview查询不会生成双链
* 注意属性的规范化
