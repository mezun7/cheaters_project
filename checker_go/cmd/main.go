package main

import (
	"checker/internal/headquater"
	"os"

	"fmt"
)

func main() {
	//fmt.Println("Diff\n", comparator.SourcesCompare([]string{""}, []string{""}))
	params := headquater.Params{
		DbHost:      os.Getenv(""),
		WorkerCount: 10,
		Local:       true,
		QueueName:   "checker",
	}

	hq, err := headquater.NewHeadquarter(params)
	if err != nil {
		fmt.Printf("failed to create hq: %w", err)
		return
	}

	hq.Start()
}
