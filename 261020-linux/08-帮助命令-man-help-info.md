# man: manual。

查看 man 的所有章节：`man man`
```text
       1   可执行程序或 shell 命令
       2   系统调用(内核提供的函数)
       3   库调用(程序库中的函数)
       4   特殊文件(通常位于 /dev)
       5   文件格式和规范，如  /etc/passwd
       6   游戏
       7   杂项（包括宏包和规范）， 如 man(7)，groff(7), man-pages(7)
       8   系统管理命令(通常只针对 root 用户)
       9   内核例程 [非标准
```

查看不同章节内的同名主题：
```bash
man 1 passwd
man 5 passwd
man -a/--all passwd
```

`man 内建命令`，比如 `man cd`，会打开所有内建命令(shell builtins)统一的手册：General Commands Manual。

# help

shell 内建命令可用 `help cd` 的格式。内外命令都可用 `cmd --help` 的格式。

查看命令类型：`type cmd`

# info

比 help 命令更详尽。
