- 已登录图形界面后进入命令行终端：sudo init 3
- 在不同的命令行终端中切换：ctrl+alt+f1~6 / sudo chvt 1~6。vt 代表 virtual terminal
- 回到图形界面：sudo init 5

init+
- 0:停机
- 1：单用户形式，只root进行维护
- 2：多用户，不能使用net file system
- 3：完全多用户
- 5：图形化
- 6：重启

终端提示符：
- #: root
- $: 普通用户

目录：
- `/etc`: 源自 et cetera （等等），现在主要存放系统级配置文件。
- `/sbin` ： system binaries ，存放系统管理、启动和修复相关命令。
- `/usr` ：最初表示 user ，早期用于存放用户目录；后来用于存放用户态程序、库和共享数据。 Unix System Resources 是后来的解释，并非原始缩写。
- `/var` ： variable ，存放运行期间经常变化的数据，如日志、缓存、队列。
- `/opt` ： optional ，存放额外安装的第三方软件包，通常每个软件独占一个子目录。
- `/proc` ： process ，虚拟文件系统，提供进程及内核运行状态信息，不存储真实磁盘文件。
- `/lib` ： libraries ，存放系统启动和基础命令所需的共享库及内核模块。现代系统中常链接到`/usr/lib` 。
