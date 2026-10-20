同步的用途有两个：
- 一个是避免多个线程在同一时刻操作同一个数据块
- 另一个是协调多个线程，以避免它们在同一时刻执行同一个代码块。

由于这样的数据块和代码块的背后都隐含着一种或多种资源（比如存储资源、计算资源、I/O 资源、网络资源等等），所以我们可以把它们看做是共享资源，或者说共享资源的代表。

我们所说的同步其实就是在控制多个线程对共享资源的访问。

只要一个代码片段需要实现对共享资源的串行化访问，就可以被视为一个临界区（critical section），

# 读写锁

读写锁是把对共享资源的“读操作”和“写操作”区别对待了。它可以对这两种操作施加不同程度的保护。换句话说，相比于互斥锁，读写锁可以实现更加细腻的访问控制。

一个读写锁中实际上包含了两个锁，即读锁和写锁。读写锁对写操作之间的互斥，其实是通过它内含的一个互斥锁实现的。因此，也可以说，Go 语言的读写锁是互斥锁的一种扩展。
- Lock, Unlock 操作写锁。加了写锁后不允许再加写锁/读锁。
- RLock, RUnlock 操作读锁。加了读锁后，不允许加写锁，但允许再加读锁。

在我们正确使用读写锁的情况下，对于某个受到读写锁保护的共享资源：
- 多个写操作不能同时进行
- 写操作和读操作也不能同时进行
- 多个读操作却可以同时进行。

互斥锁 *Mutex 实现了 sync.Locker 接口（Lock() 方法 和 Unlock() 方法）

RWMutex 组合了 w Mutex，*RWMutex 也实现了自己的 Lock/Unlock/RLock/RUnlock 方法，其 Lock/Unklock 会调用其 w 字段的相应方法+其他细节。

如何获取读写锁中的读锁？(让读锁也用 Lock/Unlock 来加/解锁) rw.RLocker():
```go
// RLocker returns a [Locker] interface that implements
// the [Locker.Lock] and [Locker.Unlock] methods by calling rw.RLock and rw.RUnlock.
func (rw *RWMutex) RLocker() Locker {
	return (*rlocker)(rw)
}

type rlocker RWMutex

func (r *rlocker) Lock()   { (*RWMutex)(r).RLock() }
func (r *rlocker) Unlock() { (*RWMutex)(r).RUnlock() }
```

互斥锁与读写锁共同的性质：
- 开箱即用
- 副本（包括传参）与原值完全没有关系。

# goroutine 让出 CPU 的一些场景

更准确的说法: 当前 goroutine 停止占用 P，让调度器运行其他可运行的 goroutine。

runtime.Gosched()：主动让出当前 P 的执行权，以允许其他 goroutine 运行(并不保证一定有其他 goroutine 被执行。)；但当前 G 仍为 runnable，不进入阻塞状态，再次被调度后继续。

runtime.GC()：强制完成一次 GC，因等待垃圾回收完成而=**阻塞**当前 goroutine。等待期间其他 goroutine 可能运行，但部分 GC 阶段也可能暂停整个程序。`GC()` 可能间接使当前 goroutine 暂停运行，但这只是垃圾回收过程的结果，不是它的调度语义。

mu.Lock()：仅锁竞争时：可能先短暂自旋；仍拿不到时因等待锁而**阻塞**当前 goroutine，P 可以运行其他 goroutine。

time.Sleep(d): 仅`d > 0`时 ：因等待定时器而**定时阻塞(休眠)**当前 goroutine，期间 P 可以运行其他 goroutine。


休眠是阻塞的一种特殊形式。
- 休眠：等待一段确定时间，例如`time.Sleep(time.Second)` 。
- 阻塞：等待某个条件成立，时间不确定，例如等待锁、channel、I/O。
- 两者都会使当前 goroutine 暂时不能运行，并释放 P 给其他 goroutine。

```text
阻塞
├── 等待定时器：time.Sleep
├── 等待锁：mu.Lock
├── 等待通信：<-ch
└── 等待 I/O
```
