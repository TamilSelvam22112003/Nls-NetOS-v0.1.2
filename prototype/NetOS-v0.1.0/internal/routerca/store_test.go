package routerca

import (
	"path/filepath"
	"testing"
)

func TestStorePersistsEnableDisable(t *testing.T) {
	s := &Store{Path: filepath.Join(t.TempDir(), "router-ca.json")}
	cfg, err := s.Load(); if err != nil { t.Fatal(err) }
	if cfg.Enabled { t.Fatal("new configuration must default to disabled") }
	cfg.Enabled = true
	if err := s.Save(cfg); err != nil { t.Fatal(err) }
	got, err := s.Load(); if err != nil { t.Fatal(err) }
	if !got.Enabled { t.Fatal("enabled state was not persisted") }
	got.Enabled = false
	if err := s.Save(got); err != nil { t.Fatal(err) }
	got, err = s.Load(); if err != nil { t.Fatal(err) }
	if got.Enabled { t.Fatal("disabled state was not persisted") }
}
