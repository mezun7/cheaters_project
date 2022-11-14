package comparator

import (
	"gorm.io/gorm"
	"io/ioutil"
	"log"
	"time"
)

type AttemptsCheckJobs struct {
	id                   int64 `gorm:"primaryKey"`
	job                  string
	attemptLhs           int
	attemptRhs           int
	scriptCheckingResult float64
	status               string
	checkingStartTime    time.Time
	checkingEndTime      time.Time
}

type Attempt struct {
	id             int64 `gorm:"primaryKey"`
	pcmsId         string
	score          int
	outcome        string
	status         string
	participant    int
	problemContest int
	time           int
	language       string
	source         string
}

func JobProcess(db *gorm.DB, jobId int64) {
	var job AttemptsCheckJobs
	db.First(&job, "id = ?", jobId)
	var attemptLhs Attempt
	db.First(&attemptLhs, "id = ?", job.attemptLhs)
	var attemptRhs Attempt
	db.First(&attemptRhs, "id = ?", job.attemptRhs)

	sourceLhs, err := ioutil.ReadFile(attemptLhs.source)
	if err != nil {
		log.Printf("Failed to read a source file, msg: %v", err)
	}
	sourceRhs, err := ioutil.ReadFile(attemptRhs.source)
	if err != nil {
		log.Printf("Failed to read a source file, msg: %v", err)
	}

	tokensLhs := Tokenize(sourceLhs, attemptLhs.source)
	tokensRhs := Tokenize(sourceRhs, attemptRhs.source)

	job.scriptCheckingResult = SourcesCompare(tokensLhs, tokensRhs)

	db.Save(&job)
}
