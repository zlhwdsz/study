# 阻塞
channel 的发送与接收都是站在外部视角来说的。

不同状态的 channel 读写表现：
- nil channel: 不可 close, 读写均阻塞。
- open channel: 读是否阻塞看缓冲区是否有数据/发送方是否发送就绪(包括 for range，只会读出或阻塞，不会退出)，写是否阻塞看缓冲区是否有空位/接收方是否接收就绪。
- closed channel：
  - 一般读一直不会阻塞：缓冲区非空时就读出正常值(以及可选的第二返回值 true)，缓冲区空后就读出零值(以及可选的第二返回值 false)。
  - for range 读：缓冲区非空时就读出正常值，**缓冲区空+closed 同时成立，for range 才会退出**。
  - 写会直接 panic

# break select/switch

不加 label 的 break，其作用对象是向上最近的 for/switch/select !

break switch/select 有什么用？主要用于： 跳出整个 switch/select(实际效果是**提前结束 case 的执行**)，然后继续执行 switch/select 后面的公共逻辑 。

```go
for {
	select {
	case v := <-ch:
		if v < 0 {
			break // 跳出 select，走下面的公共逻辑
		}
		handle(v)
	default:
		idle()
	}

	afterEachRound()
}
```

# select/switch cases 区别

select cases：选择前，所有通信操作的 channel 操作数和发送表达式按源码顺序求值一次（但并不是所有能执行的发送和接收操作都执行）。
- 有 case 的通道操作可执行？从中随机选择一个进入其分支。否则：
- 有 default(无关位置): 执行 default(故 default 可用来防止 select 阻塞)。否则：
- 阻塞直至有 case 可执行。

switch cases：按顺序求值，遇到第一个匹配项后停止。


例：

```go
package main

import "fmt"

func channel(name string) chan int {
	fmt.Println("求值通道：", name)
	return nil
}

func value() int {
	fmt.Println("求值发送值")
	return 42
}

func main() {
	select {
	case <-channel("receive"):
		fmt.Println("receive case")
	case channel("send") <- value():
		fmt.Println("send case")
	default:
		fmt.Println("default")
	}
}

/* 固定输出：
求值通道： receive
求值通道： send
求值发送值
default
*/
```