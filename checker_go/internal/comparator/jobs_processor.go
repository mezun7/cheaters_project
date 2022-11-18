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
	var job AttemptsCheckJobs
	db.First(&job, jobId)
	if db.Error != nil {
		log.Printf("Failed to read a job, msg: #{err}")
		return
	}
	job.Status = "CHECKING"

	db.Save(&job)
	if db.Error != nil {
		log.Printf("Failed to update a status, msg: #{err}")
		return
	}

	var attemptLhs Attempt
	db.First(&attemptLhs, job.AttemptLhsId)
	var attemptRhs Attempt
	db.First(&attemptRhs, job.AttemptRhsId)

	// TODO: get rid of deprecated functions
	sourceLhs, err := ioutil.ReadFile("/home/itl/cheaters_project/media/" + attemptLhs.Source)
	if err != nil {
		log.Printf("Failed to read a LHS Source file, msg: %v", err)
		return
	}
	sourceRhs, err := ioutil.ReadFile("/home/itl/cheaters_project/media/" + attemptRhs.Source)
	if err != nil {
		log.Printf("Failed to read a RHS Source file, msg: %v", err)
		return
	}

	tokensLhs := Tokenize(string(sourceLhs), attemptLhs.Source)
	tokensRhs := Tokenize(string(sourceRhs), attemptRhs.Source)

	job.ScriptCheckingResult = float64(int(SourcesCompare(tokensLhs, tokensRhs)*100)) / 100
	job.CheckingEndTime = time.Now()
	job.Status = "NOT_SEEN"

	db.Save(&job)
	if db.Error != nil {
		log.Printf("Failed to save checked job, msg: #{err}")
		return
	}
}
