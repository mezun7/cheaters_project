package main

import (
	"checker/internal/comparator"
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
	fmt.Println("Diff\n", comparator.SourcesCompare([]string{""}, []string{""}))
	params := headquater.Params{
		DbHost: os.Getenv(""),
	}

	headquater, err := headquater.NewHeadquater(params)
	if err != nil {
		fmt.Printf("failed to create headquater: %w", err)
		return
	}

	headquater.Start()
}
