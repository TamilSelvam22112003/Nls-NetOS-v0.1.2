package main

import (
	"context"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"os"
	"time"

	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/config"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/boot"
	ncrypto "github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/crypto"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/identity"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/protocol"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/routerca"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/validator"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/pkg/logging"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background()); defer cancel()
	caPath := os.Getenv("NETOS_ROUTER_CA_CONFIG"); if caPath == "" { caPath = "./runtime/router-ca.json" }
	caStore := &routerca.Store{Path: caPath}
	caCfg, err := caStore.Load(); if err != nil { panic(err) }
	if !caCfg.Enabled { fmt.Println("Router-CA disabled; onboarding not started"); return }

	cfg, err := config.Load(ctx, "config/router.yaml"); if err != nil { panic(err) }
	pass := os.Getenv(cfg.IdentityPassphraseEnv); if pass == "" { panic(fmt.Errorf("identity passphrase environment variable is empty")) }
	store := identity.FileStore{Path: cfg.IdentityStore, Passphrase: pass}
	key, cert, err := store.Load()
	if err != nil { id, x := identity.Generate(cfg.Serial, cfg.Chassis, cfg.BoardID); if x != nil { panic(x) }; key, cert = id.PrivateKey, id.CertificatePEM; if x = store.Save(key, cert); x != nil { panic(x) } }
	block, _ := pem.Decode(cert); if block == nil { panic(fmt.Errorf("invalid board certificate")) }
	clientCert, err := tls.X509KeyPair(cert, pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})); if err != nil { panic(err) }
	signer := ncrypto.Signer{PrivateKey: key, Serial: cfg.Serial, Chassis: cfg.Chassis, BoardCertificate: string(cert)}
	vc := validator.Client{DTLS: ncrypto.DTLSClient{RootCAPath: cfg.ValidatorRootCA, ClientCert: clientCert, Organization: cfg.OrganizationName}, Handshaker: protocol.ClientHandshaker{Codec: protocol.Codec{}, Signer: signer}, Timeout: cfg.ControllerTimeout}
	log := logging.New()
	seq := boot.Sequence{Log: log, Cfg: cfg, Retry: boot.RetryPolicy{Initial: cfg.RetryInitial, Max: cfg.RetryMax, Ports: []int{12346, 12347, 12348}}, Hooks: boot.Hooks{
		Handshake: func(c context.Context, a string) (protocol.Message, error) { conn, m, x := vc.Connect(c, a); if conn != nil { _ = conn.Close() }; return m, x },
		Discover: validator.Discover,
		ControllerConnect: func(context.Context, []protocol.ControllerEndpoint) error { return nil },
		FetchConfig: func(context.Context, []protocol.ControllerEndpoint) error { return nil },
	}}

	go func() {
		t := time.NewTicker(500 * time.Millisecond); defer t.Stop()
		for { select { case <-ctx.Done(): return; case <-t.C: current, e := caStore.Load(); if e == nil && !current.Enabled { fmt.Println("Router-CA disabled; stopping onboarding"); cancel(); return } } }
	}()
	if err := seq.Run(ctx); err != nil { panic(err) }
}

var _ *rsa.PrivateKey
