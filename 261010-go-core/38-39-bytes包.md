与strings.Reader类型的Len方法一样，byte.Buffer的Len方法返回的也是内容容器中未被读取部分的长度。

Cap: 容器的容量。没有 strings.Reader 一样的 Size 方法。

在bytes.Buffer中，Bytes方法和Next方法都可能会造成内容的泄露。原因在于，它们都把基于内容容器的切片直接返回给了方法的调用方。调用方拿到这个切片之后，可直接修改 Buffer 的内容！
