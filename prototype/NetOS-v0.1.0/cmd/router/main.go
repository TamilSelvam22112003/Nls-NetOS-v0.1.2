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
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.0/internal/boot"
	ncrypto "github.com/TamilSelvam22112003/Nls-NetOS-v0.1.0/internal/crypto"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.0/internal/identity"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.0/internal/protocol"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.0/internal/routerca"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.0/internal/validator"
	"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.0/pkg/logging"
)

func main() {
	ctx := context.Background()
	caPath := os.Getenv("NETOS_ROUTER_CA_CONFIG"); if caPath == "" { caPath = "./runtime/router-ca.json" }
	caStore := &routerca.Store{Path: caPath}
	for {
		cfgCA, err := caStore.Load(); if err != nil { panic(err) }
		if !cfgCA.Enabled { fmt.Println("Router-CA disabled; waiting for enable"); time.Sleep(500 * time.Millisecond); continue }
		child, cancel := context.WithCancel(ctx)
		go watchRouterCA(child, cancel, caStore)
		err = runOnboarding(child, cfgCA)
		cancel()
		if err != nil && child.Err() == nil { fmt.Printf("Router-CA onboarding stopped: %v\n", err) }
	}
}

func watchRouterCA(ctx context.Context, cancel context.CancelFunc, store *routerca.Store) {
	t := time.NewTicker(500 * time.Millisecond); defer t.Stop()
	for { select {
	case <-ctx.Done(): return
	case <-t.C:
		cfg, err := store.Load(); if err == nil && !cfg.Enabled { fmt.Println("Router-CA disabled; cancelling active onboarding"); cancel(); return }
	} }
}

func runOnboarding(ctx context.Context, ca routerca.Config) error {
	if len(ca.ValidatorAddresses) == 0 || ca.Organization == "" || ca.RootCA == "" || ca.IdentityStore == "" || ca.IdentityPassphrase == "" || ca.Serial == "" || ca.Chassis == "" || ca.BoardID == "" { return fmt.Errorf("Router-CA is enabled but its persistent configuration is incomplete") }
	cfg := config.Config{OrganizationName: ca.Organization, ValidatorAddresses: ca.ValidatorAddresses, ValidatorRootCA: ca.RootCA, IdentityStore: ca.IdentityStore, IdentityPassphraseEnv: ca.IdentityPassphrase, Serial: ca.Serial, Chassis: ca.Chassis, BoardID: ca.BoardID, ControllerTimeout: 10 * time.Second, RetryInitial: ca.RetryInitial, RetryMax: ca.RetryMax}
	pass := os.Getenv(cfg.IdentityPassphraseEnv); if pass == "" { return fmt.Errorf("identity passphrase environment variable is empty") }
	store := identity.FileStore{Path: cfg.IdentityStore, Passphrase: pass}
	key, cert, err := store.Load()
	if err != nil { id, x := identity.Generate(cfg.Serial, cfg.Chassis, cfg.BoardID); if x != nil { return x }; key, cert = id.PrivateKey, id.CertificatePEM; if x = store.Save(key, cert); x != nil { return x } }
	block, _ := pem.Decode(cert); if block == nil { return fmt.Errorf("invalid board certificate") }
	clientCert, err := tls.X509KeyPair(cert, pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})); if err != nil { return err }
	signer := ncrypto.Signer{PrivateKey: key, Serial: cfg.Serial, Chassis: cfg.Chassis, BoardCertificate: string(cert)}
	vc := validator.Client{DTLS: ncrypto.DTLSClient{RootCAPath: cfg.ValidatorRootCA, ClientCert: clientCert, Organization: cfg.OrganizationName}, Handshaker: protocol.ClientHandshaker{Codec: protocol.Codec{}, Signer: signer}, Timeout: cfg.ControllerTimeout}
	seq := boot.Sequence{Log: logging.New(), Cfg: cfg, Retry: boot.RetryPolicy{Initial: cfg.RetryInitial, Max: cfg.RetryMax, Ports: []int{12346, 12347, 12348}}, Hooks: boot.Hooks{
		Handshake: func(c context.Context, a string) (protocol.Message, error) { conn, m, x := vc.Connect(c, a); if conn != nil { _ = conn.Close() }; return m, x },
		Discover: validator.Discover,
		ControllerConnect: func(context.Context, []protocol.ControllerEndpoint) error { return nil },
		FetchConfig: func(context.Context, []protocol.ControllerEndpoint) error { return nil },
	}}
	return seq.Run(ctx)
}

var _ *rsa.PrivateKey
