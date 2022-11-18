package main

import (
	"checker/internal/headquarter"
	"os"

	"fmt"
)

func main() {
	//fmt.Println("Diff\n", comparator.SourcesCompare([]string{""}, []string{""}))
	params := headquarter.Params{
		DbHost:      os.Getenv(""),
		WorkerCount: 2,
		Local:       true,
		QueueName:   "checker",
	}

	hq, err := headquarter.NewHeadquarter(params)
	if err != nil {
		fmt.Printf("failed to create hq: %w", err)
		return
	}

	hq.Start()
}
