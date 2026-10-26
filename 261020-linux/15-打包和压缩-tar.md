# tar: tape archiver, -t 列出，-C 解包至其他目录

选项可不加 "-"（tar 传统风格，与 BSD 风格格式一致），含义与加 "-" 一致。

```text
  -c, --create               创建一个新归档
  -t, --list                 列出归档内容
  -x, --extract, --get       从归档中解出文件
  -j, --bzip2                通过 bzip2 过滤归档(.tar.bz2/.tbz2)
  -J, --xz                   通过 xz 过滤归档
  -z, --gzip, --gunzip, --ungzip   通过 gzip 过滤归档（.tar.gz/.tgz）
  -v, --verbose              详细地列出处理的文件
  -f, --file=ARCHIVE         使用归档文件或 ARCHIVE 设备
  -C, --directory=DIR        改变至目录 DIR (change directory)

Examples:
  tar -cf archive.tar foo bar  # Create archive.tar from files foo and bar.
  tar -tvf archive.tar         # List all files in archive.tar verbosely.
  tar -xf archive.tar          # Extract all files from archive.tar.
```

创建归档并压缩时，必须要指定压缩格式，否则只打包不压缩。bzip2 压缩率一般比 gzip 压缩率高一些，而 gzip 速度快、兼容性好。

查看和解压时，似乎不必指定压缩格式（能自动检测？）。

关于 -C:
```bash
tar -cf a.tar file1 -C /tmp file2 # `file1` 从原目录查找，`file2` 从`/tmp` 查找。
tar xf a.tgz -C /tmp # 将归档文件解包至 /tmp 而不是当前目录
```
