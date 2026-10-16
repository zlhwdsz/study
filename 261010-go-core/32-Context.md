Context 于 Go 1.7 加入 标准库。它的值不但可以被任意地扩散，而且还可以被用来传递额外的信息和信号。

Context 类型可以提供一类代表上下文的值。此类值是**并发安全**的，也就是说它可以被传播给多个 goroutine。

Context 是一个接口类型，有 Deadline、Done、Err、Value 四个方法。
- Done 返回的通道不是用来传递数据，而是用来感知是否取消的信号的。
- Err 在本 context 取消前返回 nil，取消后一般返回 context.Canceled / context.DeadlineExceeded。

context 包中：
- emptyCtx, backgroundCtx, todoCtx, withoutCancelCtx 等类型，都是以结构体类型为接收者实现 Context 接口。
  - `context.Background()` 生成的 backgroundCtx 仅用作充当树根，其本身不可被取消(Done 方法返回 nil)，也不能携带任何数据。
  - `context.WithoutCancel()` 生成的 withoutCancelCtx，组合 Context 作为 parent，本身不可被取消(Done 方法返回 nil)。其父子关系是单向感知的，即子知父，但父不知子。

- WithValue、WithCancel、WithTimeout、WithDeadline 等创建的 context 为结构体指针类型，相应的类型也是以指针为接收者实现 Context 接口，因为它们需要保存取消状态、定时器或键值等数据。

  - `context.WithValue()` 生成 `*valueCtx`：嵌入 Context 作为 parent。虽然其父子关系在结构上也是单向感知的，但在取消关系上父子一体，因为子未实现自己的 Done 方法，所以父子共享取消信号，**取消父就等于取消子**。
    - *valueCtx 自身只能携带一对键值（直接用字段 key 和 val 存储）。
  
  - `context.WithCancel()` 生成 `*cancelCtx`：嵌入 Context 作为 parent (调用 propagateCancel 时设置)，但父子关系是双向感知的，**取消父一定会通知到子**：

    - cancelCtx 有自己的 done 字段和 Done 方法，即子有独立的取消信号；还有 children 字段用于存放可能的子 context；还实现了 cancel 方法 / canceler 接口（cancel 方法 + 与 Context 接口相同的 Done 方法）。
  
    - 被动取消（父取消导致子取消）：`WithCancel()` 会调用 `propagateCancel()` 来建立父子之间的取消关系。
      - 若父已经取消，则直接取消自己，即调用 `child.cancel(removeFromParent: false...)`：
          - close(done)
          - 对其 children 中每个 child 调用 cancel(false), 然后清空 children(置为 nil )。（所以将子注册到 children 后，父取消时，子也会被连锁取消。）
      - 若能从 parent 开始往上找到合理 *cancelCtx，则在其 children 中注册当下的 canceler。
        - 所谓合理，是找到的 *cancelCtx 的 Done() 与 parent 相同，保证要注册 child 的祖先确实与 parent 共享取消信号。目标包括将 cancelCtx 嵌入的 *timerCtx，但会跳过 *valueCtx。
      - 略：AfterFunc 逻辑。
      - 否则，源码会退化为开 goroutine: 监听父 context 的 `Done()` channel，一旦接到该 channel 通知，就代表父 context 已经取消，则同样取消自己。

    - 主动取消(调用 cancelFunc )：`WithCancel()` 返回的第二个参数 cancelFunc 是用来主动取消相应的 context 的。当调用它时，会转而调用 `c.cancel(removeFromParent:true, err:Canceled...)`:
      - 主动取消时，会存储以及向下传递非 nil 的 err，由 Err() 返回）。
      - 除了 close(done) 与 child.cancel()、清空 children 外，主动取消时还会额外 removeChild: 尝试从从 parent 开始往上找到的合理 *cancelCtx (若存在) 的 children 中删除自己。

  - `context.WithTimeout()`、`context.WithDeadline()` 等生成 `*timeCtx`：嵌入 cancelCtx，也会调用 propagateCancel。
    - *timeCtx 既可通过调用返回的 cancelFunc 来手动取消，也可等时间到了自动取消。


上面提到各种 context，其 Value 方法会如何找值？
- *valueCtx 会先看自己是否携带了那个 key，否则返回其父的 Value 方法调用。
- backgroundCtx, todoCtx: 直接返回 nil。
- withoutCancelCtx、*cancelCtx、\*timerCtx：直接返回其父的 Value 方法调用。

Context 接口并没有提供改变数据的方法。因此，在通常情况下，我们只能通过在上下文树中添加含 *valueCtx 值来存储新的数据，或者通过取消 *valueCtx 的父值来丢弃掉相应的数据。

含数据的 context 值不能直接被取消，可取消的 context 值无法直接携带数据，但它们通过 context 树联系在一起，可以间接取消/携带数据。

