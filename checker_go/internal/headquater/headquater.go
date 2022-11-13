package headquater

import (
	cmp "checker/internal/comparator"
	"fmt"
	amqp "github.com/rabbitmq/amqp091-go"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/schema"
	"log"
	"strconv"
)

type Params struct {
	DbHost      string
	DbUser      string
	DbPassword  string
	workerCount int
	queueName   string
}

type Headquater struct {
	db   *gorm.DB
	conn *amqp.Connection

	queueName   string
	workerCount int
}

func NewHeadquater(params Params) (*Headquater, error) {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=gorm port=9920 sslmode=disable TimeZone=Asia/Shanghai",
		params.DbHost,
		params.DbUser,
		params.DbPassword,
	)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		NamingStrategy: schema.NamingStrategy{
			TablePrefix:   "checker_", // table name prefix, table for `User` would be `t_users`
			SingularTable: true,       // use singular table name, table for `User` would be `user` with this option enabled
			NoLowerCase:   true,       // skip the snake_casing of names
		},
	})
	if err != nil {
		return nil, err
	}

	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		return nil, err
	}

	return &Headquater{
		db:          db,
		conn:        conn,
		workerCount: params.workerCount,
		queueName:   params.queueName,
	}, nil
}

func (h *Headquater) Start() {
	var forever chan struct{}
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
			for d := range msgs {
				jobId, _ := strconv.Atoi(string(d.Body))
				cmp.JobProcess(h.db, int64(jobId))
			}
		}()
	}
	<-forever
}
