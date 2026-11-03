package main

import (
	"fmt"
	"os"
	"strings"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/routerca"
)

func main() {
	path := os.Getenv("NETOS_ROUTER_CA_CONFIG"); if path == "" { path = "./runtime/router-ca.json" }
	store := &routerca.Store{Path: path}
	if len(os.Args) < 2 { usage(); os.Exit(2) }
	cfg, err := store.Load(); if err != nil { fail(err) }
	switch os.Args[1] {
	case "enable": cfg.Enabled = true
	case "disable": cfg.Enabled = false
	case "status": printStatus(cfg); return
	case "set":
		if len(os.Args) != 4 { usage(); os.Exit(2) }
		if err := setField(&cfg, os.Args[2], os.Args[3]); err != nil { fail(err) }
	default: usage(); os.Exit(2)
	}
	if err := store.Save(cfg); err != nil { fail(err) }
	if cfg.Enabled { fmt.Println("Router-CA: ENABLED (persistent configuration saved)") } else { fmt.Println("Router-CA: DISABLED (persistent configuration saved)") }
}

func setField(c *routerca.Config, key, value string) error {
	switch key {
	case "validator": c.ValidatorAddresses = strings.Split(value, ",")
	case "organization": c.Organization = value
	case "root-ca": c.RootCA = value
	case "identity-store": c.IdentityStore = value
	case "identity-passphrase-env": c.IdentityPassphrase = value
	case "serial": c.Serial = value
	case "chassis": c.Chassis = value
	case "board-id": c.BoardID = value
	case "auto-enroll": if value == "true" { c.AutoEnroll = true } else if value == "false" { c.AutoEnroll = false } else { return fmt.Errorf("auto-enroll must be true or false") }
	default: return fmt.Errorf("unknown router-ca setting %q", key)
	}
	return nil
}

func printStatus(c routerca.Config) {
	state := "DISABLED"; if c.Enabled { state = "ENABLED" }
	fmt.Printf("Router-CA: %s\nValidator: %v\nOrganization: %s\nAuto-enroll: %t\n", state, c.ValidatorAddresses, c.Organization, c.AutoEnroll)
}
func usage() { fmt.Println("usage: router-ca enable|disable|status|set <validator|organization|root-ca|identity-store|identity-passphrase-env|serial|chassis|board-id|auto-enroll> <value>") }
func fail(err error) { fmt.Fprintln(os.Stderr, err); os.Exit(1) }
