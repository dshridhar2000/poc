package main

import (
	"io"
	"net/http"
)

func ssrfHandler(w http.ResponseWriter, r *http.Request) {

	url := r.URL.Query().Get("url")

	// Vulnerable
	resp, _ := http.Get(url)
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)

	w.Write(body)
}
