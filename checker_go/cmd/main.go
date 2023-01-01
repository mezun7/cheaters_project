package main

import (
	"checker/internal/headquarter"
	"os"

	"fmt"
)

func main() {
	//fmt.Println("Diff\n", comparator.SourcesCompare([]string{""}, []string{""}))
	params := headquarter.Params{
		DbHost:     os.Getenv("DB_HOST"),
		DbPort:     os.Getenv("DB_PORT"),
		DbUser:     os.Getenv("POSTGRES_USER"),
		DbPassword: os.Getenv("POSTGRES_PASSWORD"),
		DbName:     os.Getenv("POSTGRES_DB"),

		WorkerCount:   2,
		QueueName:     os.Getenv("CHECKER_QUEUE_NAME"),
		SourcesPrefix: os.Getenv("CHECKER_SOURCES_PREFIX"),
		RmqHost:       os.Getenv("RMQ_HOST"),
	}

	hq, err := headquarter.NewHeadquarter(params)
	if err != nil {
		fmt.Printf("failed to create hq: %w", err)
		return
	}

	hq.Start()
}
