在 GOPATH 时代，Go 语言的源码文件都需要被存放在环境变量 GOPATH 包含的某个工作区（目录）中的 src 目录下的某个代码包（目录）中。一个代码包的导入路径实际上就是从 src 子目录，到该包的实际存储位置的相对路径。

Go 包有“子目录里的包”，但没有 Java 那种“子包继承父包作用域”的概念:
- 包的边界是目录，不是命名层级。
- 父目录包和子目录包彼此独立，使用时仍然要`import` 。
- 可见性只由名字首字母决定：大写导出，小写仅当前包可见。
- `internal` 目录比较特殊，可以限制导入范围（仅导入路径以 internal 父目录开头的包，才能导入 internal 目录下的包），但它也不是“子包继承”。

在 Go Modules 时代， GOPATH 配置依然发挥的作用：
- GOPATH 默认值为 ~/go。
- go install 的默认落点为 GOPATH/bin，可被 GOBIN 覆盖。
- 模块缓存的落点 GOMODCHACHE 默认为 GOPATH/pkg/mod。

一句 `import "importpath"`, go 会从哪里去找依赖包？如何使用依赖包？

首先，弄懂 importpath:
- 它要么是"相对 $GOROOT/src 的相对路径"，即标准库(相当于省略特殊模块名 `std`)，要么是"普通模块名+相对模块根目录(go.mod所在目录)的相对路径"。
- 模块名不一定等于目录名，但 importpath 里模块名之外的其他部分都是目录名。
- 模块名要么是当前模块（源文件一路上溯遇到的第一个包含 go.mod 的目录）本身的名字（go.mod 中 module 语句声明的名字），要么是当前模块的依赖图中的模块名（go.mod 中 require 语句声明的名字；replace 语句不改变模块名，只改变模块所处的位置）。
- importpath 里的最后部分不一定等于包名。
  - 有可能整个 importpath 就是模块名而不包括相对路径，此时包就对应模块根目录本身，而且不一定是 main 包。见 [01-pkgatmod](mods/01-pkgatmod/go.mod)。
  - 若 importpath 包含相对路径，那其最后部分一定是目录名，但包名(package 语句声明)不一定等于该目录名。
  - 代码中要使用包名而不是目录名。Go 允许二者不一致，但为避免引起疑惑，一般不要让它们不一致；非得不一致，则一般采用 `import alias "importpath"` 的书写形式。

根据 importpath 寻找包：
- 先在标准库内查找。
- 再看是不是当前 module 里的包。
- 再看是不是当前 workspace 里的 module 里的包。
- 再看是不是当前 module 的外部依赖(require 定义)，源码通常在模块缓存 GOMODCACHE 里，若无则尝试下载。

可以用这个命令看一个 importpath 最终解析到了哪个目录：
```bash
go list -f '{{.ImportPath}} => {{.Dir}}' importpath
```
