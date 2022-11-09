package main

import (
	"log"
	"net"
	"net/http"
)

var conn net.Conn

func root(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("hi"))
	return
}

func sendDataToAI(w http.ResponseWriter, r *http.Request) {
	img_data := []byte{5, 25, 255, 17}
	conn.Write(img_data)

	bufr := make([]byte, 784)
	conn.Read(bufr)
	w.Write([]byte("data writter to ai"))
}

func main() {
	var err error
	conn, err = net.Dial("tcp", "localhost:5533")
	defer conn.Close()

	if err != nil {
		log.Println("failed to get socket connection")
		log.Println(err)
		return
	}

	http.HandleFunc("/", root)
	http.HandleFunc("/ai", sendDataToAI)
	log.Println("the server started on http://localhost:4000")
	log.Println(http.ListenAndServe(":4000", nil))
}
