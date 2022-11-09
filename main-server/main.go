package main

import (
	"encoding/binary"
	"fmt"
	"log"
	"net"
	"net/http"
)

func root(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("hi"))
	return
}

func sendDataToAI(w http.ResponseWriter, r *http.Request) {
	conn, err := net.Dial("tcp", "localhost:5533")

	if err != nil {
		log.Println("failed to get socket connection")
		log.Println(err)
		return
	}
	defer conn.Close()

	img_data := make([]byte, 784)

	conn.Write(img_data)

	bufr := make([]byte, 2)
	conn.Read(bufr)

	if bufr == nil {
		log.Println("nil bufr")
		return
	}

	ans := binary.BigEndian.Uint16(bufr)

	log.Println(ans)

	w.Write([]byte(fmt.Sprint(ans)))
}

func main() {
	http.HandleFunc("/", root)
	http.HandleFunc("/ai", sendDataToAI)
	log.Println("the server started on http://localhost:4000")
	log.Println(http.ListenAndServe(":4000", nil))
}
