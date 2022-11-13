package main

import (
	"checker/internal/headquater"
	"os"

	"fmt"
)

/*
type Source struct {
    file string
    relativePath string
    userId string
    problemId string
    runId string
    attempt int
    score int
    tokens []string
    compare bool
}
*/

func main() {
	//fmt.Println("Diff\n", comparator.SourcesCompare([]string{""}, []string{""}))
	params := headquater.Params{
		DbHost: os.Getenv(""),
	}

	hq, err := headquater.NewHeadquater(params)
	if err != nil {
		fmt.Printf("failed to create hq: %w", err)
		return
	}

	hq.Start()
}
