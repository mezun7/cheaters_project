package headquater

import (
	"fmt"
	amqp "github.com/rabbitmq/amqp091-go"
	"gorm.io/gorm"
	"log"
)

type Params struct {
	DbHost      string
	DbUser      string
	DbPassword  string
	workerCount int
}

type Headquater struct {
	db          *gorm.DB
	conn        *amqp.Connection
	workerCount int
}

func NewHeadquater(params Params) (*Headquater, error) {
	dsn := fmt.Sprintf("host=%s user=%s password=%s dbname=gorm port=9920 sslmode=disable TimeZone=Asia/Shanghai",
		params.DbHost,
		params.DbUser,
		params.DbPassword,
	)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
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
	}, nil
}

func (h *Headquater) Start() {
	var forever chan struct{}
	for i := 0; i < h.workerCount; i++ {
		go func() {
			ch, _ := h.conn.Channel()
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
				log.Printf("Received a message: %s", d.Body)
			}
		}()
	}
	<-forever
}
