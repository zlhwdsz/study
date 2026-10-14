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

互斥锁 Mutex 实现了 sync.Locker 接口（Lock() 方法 和 Unlock() 方法）

RWMutex 组合了 Mutex，也实现了自己的 Lock/Unlock/RLock/RUnlock 方法。

如何获取读写锁中的读锁？(让读锁也用 Lock/Unlock 来加/解锁)
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
