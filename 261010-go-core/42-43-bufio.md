bufio.Reader:
- Peek方法的特点是即使读取了缓冲区中的数据，也不会更改已读计数的值。
- Read方法会在参数值的长度过大，且缓冲区中已无未读字节时，跨过缓冲区并直接向底层读取器索要数据。
- ReadSlice方法会在缓冲区的未读部分中寻找给定的分隔符，并在必要时对缓冲区进行填充。找分隔符后**返回内部缓冲区切片**。如果在一次填满缓冲区之后仍然未能找到分隔符，那么该方法就会把整个缓冲区作为第一个结果值返回，同时返回 ErrBufferFull。
  - ReadLine 基于它实现。
- ReadBytes方法会通过调用ReadSlice方法，一次又一次地填充缓冲区，并在其中寻找分隔符。找到分隔符后返回独立的`[]byte`。除非发生了未预料到的错误或者找到了分隔符，否则这一过程将会一直进行下去。
  - ReadString 基于它实现。

Peak、ReadSlice、ReadLine 可能会造成缓冲区中的内容泄露。

bufio.Scanner 与 bufio.Reader 的异同：两者都会包装`io.Reader` 并进行缓冲读取，但抽象层级不同。
- `bufio.Reader` 面向字节流控制
- `bufio.Scanner` 面向 token 迭代。抽象层级：行 / 单词 / 自定义 token（by 自定义`SplitFunc`）
