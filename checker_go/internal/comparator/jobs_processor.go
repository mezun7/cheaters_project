package comparator

import (
	"gorm.io/gorm"
	"io/ioutil"
	"log"
	"time"
)

type AttemptsCheckJobs struct {
	ID                   uint `gorm:"primaryKey"`
	JobId                string
	AttemptLhsId         int
	AttemptRhsId         int
	ScriptCheckingResult float64
	Status               string
	CheckingStartTime    time.Time
	CheckingEndTime      time.Time
}

func (AttemptsCheckJobs) TableName() string {
	return "checker_attemptscheckjobs"
}

type Attempt struct {
	ID               uint `gorm:"primaryKey"`
	PcmsId           string
	Score            int
	Outcome          string
	Status           string
	ParticipantId    int64
	ProblemContestId int64
	Time             int
	Language         string
	Source           string
	Alias            int
}

func (Attempt) TableName() string {
	return "checker_attempt"
}

func JobProcess(db *gorm.DB, jobId int64) {
	err := db.Transaction(func(tx *gorm.DB) error {
		var job AttemptsCheckJobs
		db.First(&job, jobId)
		// TODO: this is useless inside a transaction
		job.Status = "CHECKING"

		var attemptLhs Attempt
		db.First(&attemptLhs, job.AttemptLhsId)
		var attemptRhs Attempt
		db.First(&attemptRhs, job.AttemptRhsId)

		// TODO: get rid of deprecated functions
		sourceLhs, err := ioutil.ReadFile("/home/itl/cheaters_project/media/" + attemptLhs.Source)
		if err != nil {
			log.Printf("Failed to read a Source file, msg: %v", err)
			return err
		}
		sourceRhs, err := ioutil.ReadFile("/home/itl/cheaters_project/media/" + attemptRhs.Source)
		if err != nil {
			log.Printf("Failed to read a Source file, msg: %v", err)
			return err
		}

		tokensLhs := Tokenize(string(sourceLhs), attemptLhs.Source)
		tokensRhs := Tokenize(string(sourceRhs), attemptRhs.Source)

		job.ScriptCheckingResult = float64(int(SourcesCompare(tokensLhs, tokensRhs)*100)) / 100
		job.CheckingEndTime = time.Now()
		job.Status = "NOT_SEEN"

		db.Save(&job)
		return nil
	})
	if err != nil {
		log.Printf("Transaction failed, msg: #{err}")
		return
	}
}
