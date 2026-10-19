map 的 value 类型不限。但 map 要保证 key 的唯一性，所以 key 的类型必须支持同类型之间“==”和“!=”两种比较操作符，即 comparable / hashable。

不支持作为 key 的类型有：
- slice/map/func (另一方面，它们只支持与 nil 进行比较)
- 元素不被支持的数组、有字段不被支持的结构体 (同时，它们不支持与 nil 进行比较)

 注意：指针、channel、interface 类型都是 comparable。但若 key 为 interface 类型，其底层类型又是 unhashable 的，则会通过编译检查，但会产生运行时 panic！
 
 map 的底层实现：
 - Go 1.24 以前：桶链结构
 - Go 1.24+: Swiss Table
