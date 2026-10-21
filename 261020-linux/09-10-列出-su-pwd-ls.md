# su: substitue user

```bash
su alice   # 切换到 alice
su - alice # 切换并加载 alice 的完整登录环境
su         # 切换到 root, 只切换用户身份，通常保留当前目录和较多原用户环境，启动 非登录 Shell 。
su -       # 等同于`su --login` ，模拟 root 重新登录：
# - 切换到`/root`
# - 使用 root 的`HOME` 、`PATH` 等环境
# - 加载 root 的登录配置文件切换并加载 root 的完整登录环境
```

# pwd: print working directory

- -P: 打印当前的物理(physical)目录，而不包含任何的符号链接。

# ls: list, -t 时间排列, -r 逆序，-R 递归

- ‘-l’，‘--format=long’, ‘--format=verbose’
- -a, --all, 不要隐藏以 . 开头的项目
- -A, --almost-all，列出除 . 及 .. 以外的所有项目
- -r, --reverse，排序时逆序排列（默认按 alphabetic 排列）
- -R, --recursive，递归地列出子目录（直到最底层）
- -t, 按时间排列（顺序：从新到旧，逆序：从旧到新）
- -d, --directory，列出目录本身，而不是目录的内容
- -h, --human-readable，同时使用 -l 或 -s 时，将大小表示为 1K 234M 2G 等
