package main

import (
	"io/ioutil"
	"log"
	"net"
	"net/http"

	"github.com/rs/cors"
)

func root(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("hi"))
	return
}

func sendDataToAI(w http.ResponseWriter, r *http.Request) {
	req_buf, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Println("failed to read request body")
		log.Println(err)
		return
	}

	conn, err := net.Dial("tcp", "localhost:5533")
	if err != nil {
		log.Println("failed to get socket connection")
		log.Println(err)
		return
	}
	defer conn.Close()

	img_data := req_buf

	conn.Write(img_data)

	send_buf := make([]byte, 2)
	conn.Read(send_buf)

	if send_buf == nil {
		log.Println("nil bufr")
		return
	}

	w.Write(send_buf)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", root)
	mux.HandleFunc("/ai", sendDataToAI)

	handler := cors.Default().Handler(mux)

	log.Println("the server started on http://localhost:4000")
	log.Println(http.ListenAndServe(":4000", handler))
}
