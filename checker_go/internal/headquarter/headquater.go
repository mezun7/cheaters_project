package headquarter

import (
	cmp "checker/internal/comparator"
	"fmt"
	amqp "github.com/rabbitmq/amqp091-go"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"log"
	"strconv"
)

type Params struct {
	DbHost     string
	DbUser     string
	DbPassword string
	DbName     string
	DbPort     string

	WorkerCount int
	QueueName   string

	SourcesPrefix string
}

type Headquarter struct {
	db   *gorm.DB
	conn *amqp.Connection

	queueName     string
	workerCount   int
	sourcesPrefix string
}

func NewHeadquarter(params Params) (*Headquarter, error) {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable TimeZone=Europe/Moscow",
		params.DbHost,
		params.DbUser,
		params.DbPassword,
		params.DbName,
		params.DbPort,
	)
	log.Printf("Postgres dsn: %s", dsn)
	db, err := gorm.Open(postgres.Open(dsn))
	if err != nil {
		return nil, err
	}

	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		return nil, err
	}

	log.Printf("DEBUG: successfully connected to DB and RMQ")

	return &Headquarter{
		db:   db,
		conn: conn,

		workerCount: params.WorkerCount,
		queueName:   params.QueueName,

		sourcesPrefix: params.SourcesPrefix,
	}, nil
}

func (h *Headquarter) Start() {
	var forever chan struct{}
	log.Printf("Running %v workers", h.workerCount)
	for i := 0; i < h.workerCount; i++ {
		go func() {
			ch, _ := h.conn.Channel()
			defer func(ch *amqp.Channel) {
				err := ch.Close()
				if err != nil {
					log.Printf("Failed to close a channel, msg: %v", err)
				}
			}(ch)
			q, err := ch.QueueDeclare(
				h.queueName, // name
				true,        // durable
				false,       // delete when unused
				false,       // exclusive
				false,       // no-wait
				nil,         // arguments
			)
			if err != nil {
				log.Printf("Failed to create a queue, msg %v", err)
				return
			}
			msgs, err := ch.Consume(
				q.Name, // queue
				"",     // consumer
				true,   // auto-ack
				false,  // exclusive
				false,  // no-local
				false,  // no-wait
				nil,    // args
			)
			if err != nil {
				return
			}
			log.Printf("Start jobs consuming...")
			for d := range msgs {
				jobId, _ := strconv.Atoi(string(d.Body))
				log.Printf("Processing jobId=%v", jobId)
				cmp.JobProcess(h.db, int64(jobId), h.sourcesPrefix)
			}
		}()
	}
	<-forever
}
