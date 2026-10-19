ASCII 编码方案：使用单个字节（byte）的二进制数来编码一个字符。
- 标准的 ASCII 编码用一个字节的最高比特（bit）位作为奇偶校验位。
- 扩展的 ASCII 编码则将此位也用于表示字符。

UTF-8、UTF-16 和 UTF-32，- 后面的数字，表示以多少个比特作为一个编码单元。

UTF-8 与标准的 ASCII 编码是完全兼容的：在[0x00, 0x7F]的范围内，这两种编码表示的字符都是相同的。

UTF-8 是一种可变宽的编码方案。换句话说，它会用一个或多个字节的二进制数来表示某个字符，最多使用四个字节。比如，对于一个英文字符，它仅用一个字节的二进制数就可以表示，而对于一个中文字符，它需要使用三个字节才能够表示。不论怎样，一个受支持的字符总是可以由 UTF-8 编码为一个字节序列。

UTF-8编码字节含义： 对于UTF-8编码中的任意字节B：
- 如果B的第一位为0，则B独立的表示一个字符(ASCII码)；
- 如果B的第一位为1，第二位为0，则B为一个多字节字符中的一个字节(非ASCII字符)；
- 如果B的前两位为1，第三位为0，则B为两个字节表示的字符中的第一个字节；
- 如果B的前三位为1，第四位为0，则B为三个字节表示的字符中的第一个字节；
- 如果B的前四位为1，第五位为0，则B为四个字节表示的字符中的第一个字节

string 底层：由一系列相对应的 Unicode 代码点(rune)的 UTF-8 编码值(byte)。

string 的索引一定是 byte 视角，哪怕是 for range string：遍历的是 rune，索引却仍是 byte 视角（所以可能不连续）。

取得一个字符的 utf-8 编码字节数：

```go
import "unicode/utf8"

func main() {
	println(utf8.RuneLen('1')) // 1
    println(utf8.RuneLen('我')) // 3
}
```

Go 与 Python 的字符串实现对比：
- 字面值：
  - Go 中单引号为 rune literal, 双引号为 string literal。
  - Python 没有独立的字符类型，`'好'` 和`"好"` 都是长度为 1 的`str` 。
- 底层：
  - Go 中 string 的底层就是 utf-8 编码的 []byte, len(string)、索引都是字节视角。
  - Python 中 str 底层根据字符串中的最大码点选择统一宽度(1/2/4字节)，len(str)、索引都是字符视角。绝大部分常用汉字都位于 Unicode 基本多文种平面（BMP，`U+0000～U+FFFF` ），能用2字节表示。
    - `bytes(str,必填encoding)` / `str.encode(encoding默认utf8)` 将 str 转换为 bytes
    - `str(bytes,encoding)` / `bytes.decode(encoding默认为utf8)` 将 bytes 转换为 str。
