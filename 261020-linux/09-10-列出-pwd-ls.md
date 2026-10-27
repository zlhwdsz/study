# pwd: print working directory

- -P: 打印当前的物理(physical)目录，而不包含任何的符号链接。

# ls: list, -t 时间排列, -r 逆序，-R 递归

- ‘-l’，‘--format=long’, ‘--format=verbose’
- -s, --size, 显示给每个文件分配的大小，单位为块
- -a, --all, 不要隐藏以 . 开头的项目
- -A, --almost-all，列出除 . 及 .. 以外的所有项目
- -r, --reverse，排序时逆序排列（默认按 alphabetic 排列）
- -R, --recursive，递归地列出子目录（直到最底层）
- -t, 按时间排列（顺序：从新到旧，逆序：从旧到新）
- -d, --directory，列出目录本身，而不是目录的内容
- -h, --human-readable，同时使用 -l 或 -s 时，将大小表示为 1K 234M 2G 等
  - --si（Système international d'unités, International System of Units, 国际单位制），类似，但是使用 1000 的幂，而不是 1024
- -L, --dereference，当显示符号链接的文件信息时，显示符号链接指向
- -i, --inode                显示每个文件的索引编号（inode 号）
