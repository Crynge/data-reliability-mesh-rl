package main

import (
	"encoding/json"
	"net/http"
)

type Status struct {
	Service string `json:"service"`
	Status  string `json:"status"`
}

func main() {
	http.HandleFunc("/health", func(w http.ResponseWriter, _ *http.Request) {
		_ = json.NewEncoder(w).Encode(Status{Service: "lineage-builder", Status: "ok"})
	})
	_ = http.ListenAndServe(":8091", nil)
}

