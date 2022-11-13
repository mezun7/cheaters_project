package comparator

import (
	"gorm.io/gorm"
)

type AttemptsCheckJobs struct {
	id                   int64 `gorm:"primaryKey"`
	job                  string
	attemptLhs           string
	attemptRhs           string
	scriptCheckingResult string
	status               string
	checkingStartTime    string
	checkingEndTime      string
}

type Attempt struct {
	id             int64 `gorm:"primaryKey"`
	pcmsId         string
	score          string
	outcome        string
	status         string
	participant    string
	problemContest string
	time           int
	language       string
	source         string
}

func JobProcess(db *gorm.DB, jobId int64) {
	var job AttemptsCheckJobs
	db.First(&job, "id = ?", jobId)

	// TODO: run comparing

	db.Save(&job)
}
