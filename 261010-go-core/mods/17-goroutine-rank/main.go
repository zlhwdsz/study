package main

import "fmt"

const NUM_OF_WORKERS = 10

func main() {
	signals := make([]chan struct{}, NUM_OF_WORKERS+1)
	for i := range NUM_OF_WORKERS + 1 {
		signals[i] = make(chan struct{})
	}

	for i := range NUM_OF_WORKERS {
		go func() {
			<-signals[i]
			defer func() {
				signals[i+1] <- struct{}{}
			}()
			fmt.Println(i)
		}()
	}

	signals[0] <- struct{}{}
	<-signals[NUM_OF_WORKERS]
}
