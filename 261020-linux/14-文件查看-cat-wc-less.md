# cat: concatenate

原本用于连接多个文件并输出，因为也能输出单个文件，所以常被用来查看文件内容。

# wc: word count, -m 字符数, -c 字节数

默认输出行数(-l)、单词数(-w)、字节数(-c)、文件名 。

```bash
  -l, --lines            输出换行符数
  -L, --max-line-length  输出最长行的长度
  -w, --words            输出单词数(由空白字符或者输入的开始或结束分隔的、非空的、由非空白字符构成的字符序列。)
  -m, --chars            输出字符数
  -c, --bytes            输出字节数
```

注：历史兼容：早期 Unix 主要使用 ASCII， 1 个字符 = 1 个字节 ，所以`-c` 原本表示 character count。出现 UTF-8 等多字节编码后，一个字符可能占多个字节。为避免破坏旧脚本，`-c` 保留原来的“字节数”行为，新增`-m` 统计字符数。`m` 可记作 multibyte character。

# more & less, ? 向上搜索, 100g 跳行

两者都用于 分页查看文本 ，核心区别是：

- `more` ：较早、简单，以向前浏览为主，回退能力因实现而异。
- `less` ：功能更多，可自由前后翻页、双向搜索和快速跳转，日常更推荐。

名字`less` 来自一句双关语： less is more 。实际上`less` 比`more` 功能更多。

`less` 选项：
```text
  -m  -M  ....  --long-prompt  --LONG-PROMPT
                  Set prompt style.
  -n .........  --line-numbers
                  Suppress line numbers in prompts and messages.
  -N .........  --LINE-NUMBERS
                  Display line number at start of each line.
```

`less` 常用按键：
```text
Space / PageDown  下一页
b / PageUp        上一页
/关键字           向文件末尾搜索
?关键字           向文件开头搜索
n(ext) / N       下 / 上一个匹配行
g(o to line) / G 文件开头 / 末尾
数字g(不用按回车)  跳转到特定行
q                 退出
```
