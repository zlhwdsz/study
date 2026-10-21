# su: substitue user

```bash
su alice   # 切换到 alice
su - alice # 切换并加载 alice 的完整登录环境
su -       # 切换到 root
su         # 切换到 root
```

# pwd: print working directory

- -P: 打印当前的物理(physical)目录，而不包含任何的符号链接。

# ls: list

- ‘-l’，‘--format=long’, ‘--format=verbose’
- -a, --all, 不要隐藏以 . 开头的项目
- -A, --almost-all，列出除 . 及 .. 以外的所有项目
- -r, --reverse，排序时逆序排列（默认按 alphabetic 排列）
- -R, --recursive，递归地列出子目录（直到最底层）
- -t, 按时间排列（顺序：从新到旧，逆序：从旧到新）
- -d, --directory，列出目录本身，而不是目录的内容
