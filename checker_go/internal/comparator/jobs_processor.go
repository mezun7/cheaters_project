package comparator

import (
	"gorm.io/gorm"
	"io/ioutil"
	"log"
	"time"
)

type AttemptsCheckJobs struct {
	id                   int `gorm:"primaryKey"`
	jobId                string
	attemptLhsId         int
	attemptRhsId         int
	scriptCheckingResult float64
	status               string
	checkingStartTime    time.Time
	checkingEndTime      time.Time
}

func (AttemptsCheckJobs) TableName() string {
	return "checker_attemptscheckjobs"
}

type Attempt struct {
	id               int `gorm:"primaryKey"`
	pcmsId           string
	score            int
	outcome          string
	status           string
	participantId    int64
	problemContestId int64
	time             int
	language         string
	source           string
	alias            int
}

func (Attempt) TableName() string {
	return "checker_attempt"
}

func JobProcess(db *gorm.DB, jobId int64) {
	err := db.Transaction(func(tx *gorm.DB) error {
		var job AttemptsCheckJobs
		db.First(&job, "id = ?", jobId)
		job.status = "CHECKING"

		var attemptLhs Attempt
		db.First(&attemptLhs, "id = ?", job.attemptLhsId)
		var attemptRhs Attempt
		db.First(&attemptRhs, "id = ?", job.attemptRhsId)

		sourceLhs, err := ioutil.ReadFile(attemptLhs.source)
		if err != nil {
			log.Printf("Failed to read a source file, msg: %v", err)
			return err
		}
		sourceRhs, err := ioutil.ReadFile(attemptRhs.source)
		if err != nil {
			log.Printf("Failed to read a source file, msg: %v", err)
			return err
		}

		tokensLhs := Tokenize(string(sourceLhs), attemptLhs.source)
		tokensRhs := Tokenize(string(sourceRhs), attemptRhs.source)

		job.scriptCheckingResult = float64(int(SourcesCompare(tokensLhs, tokensRhs)*100)) / 100
		job.checkingEndTime = time.Now()
		job.status = "NOT_SEEN"

		db.Save(&job)
		return nil
	})
	if err != nil {
		log.Printf("Transaction failed, msg: #{err}")
		return
	}
}
