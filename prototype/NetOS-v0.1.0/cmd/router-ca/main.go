package main

import (
	"fmt"
	"os"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/routerca"
)

func main() {
	path := os.Getenv("NETOS_ROUTER_CA_CONFIG")
	if path == "" { path = "./runtime/router-ca.json" }
	store := &routerca.Store{Path: path}
	if len(os.Args) < 2 { fmt.Fprintln(os.Stderr, "usage: router-ca {enable|disable|status}"); os.Exit(2) }
	cfg, err := store.Load(); if err != nil { fmt.Fprintln(os.Stderr, err); os.Exit(1) }
	switch os.Args[1] {
	case "enable":
		cfg.Enabled = true
		if err := store.Save(cfg); err != nil { fmt.Fprintln(os.Stderr, err); os.Exit(1) }
		fmt.Println("Router-CA: ENABLED (persistent configuration saved)")
	case "disable":
		cfg.Enabled = false
		if err := store.Save(cfg); err != nil { fmt.Fprintln(os.Stderr, err); os.Exit(1) }
		fmt.Println("Router-CA: DISABLED (persistent configuration saved)")
	case "status":
		state := "DISABLED"; if cfg.Enabled { state = "ENABLED" }
		fmt.Printf("Router-CA: %s\n", state)
	default:
		fmt.Fprintln(os.Stderr, "unknown command")
		os.Exit(2)
	}
}
