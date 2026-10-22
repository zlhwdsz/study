# su: substitue user

```bash
su alice   # 只切换用户身份(默认 root)，通常保留当前目录和较多原用户环境，启动 非登录 Shell 。
su - alice # 切换并加载用户(默认 root)的完整登录环境，等同于`su --login，摸拟重新登录：
# - 切换到家目录
# - 使用用户的 的`HOME` 、`PATH` 等环境
# - 加载用户的登录配置文件切换并加载用户的完整登录环境
```

# sudo: supersuer do -> substitue user do

原本是 superuser do ，意为“以超级用户身份执行”。现在它也能通过`-u` 指定其他用户，因此也常解释为 substitute user do.

```bash
sudo command        # 默认以 root 执行
sudo -u alice command  # 以 alice 执行。-g 指定用户组。
```

使用 `visudo` 安全编辑 sudo 授权规则文件 /etc/sudoers：
- 锁定`/etc/sudoers` ，避免多人同时修改。
- 使用文本编辑器打开配置。
- 保存前检查语法。
- 语法错误时阻止直接安装错误配置，避免所有人都无法使用`sudo`。

编辑独立规则文件：`sudo visudo -f /etc/sudoers.d/alice`

/etc/sudoers 文件格式：

```text
用户或%用户组  主机=(目标用户:目标组)  [标签:] 命令列表
```

- 用户或用户组：用户名表示单个用户，组名前加 `%`，如 `alice`、`%wheel`。
- 主机：规则在哪些主机上生效，单机配置通常写 `ALL`。
- 目标用户和目标组：允许通过 `sudo` 切换成谁；
  - `(ALL)` ：可以切换为任意用户；组未单独放开，只能使用该目标用户(而不是执行命令的用户)所属的组。
  - `(ALL:ALL)` ：目标用户和目标组都可以任意组合，比`(ALL)` 权限更宽。`sudo -u bob -g docker command`：即使`bob` 不属于`docker` 组，也可以执行。
  - `(:ALL)` ：省略目标用户，表示仍以当前调用者身份运行，但允许切换为任意组。
- 标签：可选，如 `NOPASSWD:` 表示执行后续命令时不验证当前用户的密码；默认通常需要验证。
- 命令列表：允许执行的命令，以逗号分隔；应使用绝对路径，`ALL` 表示任意命令。

```sudoers
alice   ALL=(ALL:ALL) ALL
%wheel  ALL=(ALL)     ALL
alice   ALL=(root) NOPASSWD: /usr/bin/systemctl restart nginx
```

第一条允许 `alice` 以任意用户和组执行任意命令；第二条对 `wheel` 组授权；第三条只允许 `alice` 以 `root` 身份免密重启 nginx。应使用 `visudo` 或 `visudo -f` 修改规则，不要直接编辑。

另：一般安装操作系统时添加的普通用户都赋予了附加用户组 wheel (特权组，英语俚语 big wheel ，指“有权势、有影响力的人”)，然后 /etc/sudoers 里有：
```bash
## Allows people in group wheel to run all commands
%wheel  ALL=(ALL)       ALL
```

给用户添加所有 sudo 命令，可直接将该用户加入 wheel 用户组：`sudo usermod -aG wheel alice`。
