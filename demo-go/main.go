package main

import "fmt"

func main() {
	a := [3]int{1, 2, 3}
	b := a[:2]
	_ = append(b, 4)
	fmt.Println(a[2], b)
}
