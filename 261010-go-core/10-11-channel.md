channel 的发送与接收都是站在外部视角来说的。

不同状态的 channel 读写表现：
- nil channel: 不可 close, 读写均阻塞。
- open channel: 读是否阻塞看缓冲区是否有数据/发送方是否发送就绪(包括 for range，只会读出或阻塞，不会退出)，写是否阻塞看缓冲区是否有空位/接收方是否接收就绪。
- closed channel：
  - 一般读一直不会阻塞：缓冲区非空时就读出正常值(以及可选的第二返回值 true)，缓冲区空后就读出零值(以及可选的第二返回值 false)。
  - for range 读：缓冲区非空时就读出正常值，**缓冲区空+closed 同时成立，for range 才会退出**。
  - 写会直接 panic

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
