---

---

Obsidian资料库的查询工具
## 什么时候使用到查询：
* 条件复杂
* 基于内容的元数据查询
* 需要保存查询结果
* 一次查询，持续使用
## 能做到什么：
* 以不同视图展示
* 复杂条件查询
* 汇总
* 操作
## 语法
* 声明代码块dataview
* 指定查询展示的方式(如list)
* 指定从哪里进行查询from "Obsidian内文件夹路径",标签则是#标签名

```dataview
list 
from "00 InBox" and #入门 

```
* 查询展示的方式
	* list：列表
	* table:表格
	* task:任务
	* calender:日历视图
* 条件叠加
	* or
	* and
* Where
	* 添加一个或多个可用(不)等式表达的条件
	* 对于自定义rating属性的查询
* Sort（sort file.name/file.ctime(即排序的依据) asc)
	* desc:降序
	* asc:升序

### 查询的视图

* list
	* 无序列表
	* 除ID列外，只能有一个列(可以在list 后加上其他列，如tags,让其展示标签)
* table
	* 可以展示多个其他列(table tags,file.name,……)
		* file.name 文件标题
		* file.folder 文件所属文件夹路径
		* file.path 文件路径
		* file.size(in bytes) 文件大小
		* file.ctime 文件创建时间
		* file.mtime 文件修改时间
		* file.cday 创建日期
		* file.mday 修改日期
		* file.tags 笔记所有标签数组
	* 如果英文太复杂，可以在某个列后面加 as "中文别名"
	* 在table 后面加without ID，就可以不显示ID列
	* 查看当前文件所有属性：(如下)
```dataview
table this
where file=this.file
limit 1
```