package routerca

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sync"
)

// Store persists Router-CA configuration on local nonvolatile storage.
type Store struct { Path string; mu sync.Mutex }

// Load reads the configuration. A missing file returns disabled defaults.
func (s *Store) Load() (Config, error) {
	s.mu.Lock(); defer s.mu.Unlock()
	cfg := DefaultConfig()
	b, err := os.ReadFile(s.Path)
	if os.IsNotExist(err) { return cfg, nil }
	if err != nil { return cfg, fmt.Errorf("router-ca load: %w", err) }
	if err := json.Unmarshal(b, &cfg); err != nil { return cfg, fmt.Errorf("router-ca decode: %w", err) }
	return cfg, nil
}

// Save atomically persists Router-CA configuration.
func (s *Store) Save(cfg Config) error {
	s.mu.Lock(); defer s.mu.Unlock()
	if s.Path == "" { return fmt.Errorf("router-ca store path is empty") }
	b, err := json.MarshalIndent(cfg, "", "  "); if err != nil { return fmt.Errorf("router-ca encode: %w", err) }
	if err := os.MkdirAll(filepath.Dir(s.Path), 0700); err != nil { return fmt.Errorf("router-ca mkdir: %w", err) }
	tmp := s.Path + ".tmp"
	if err := os.WriteFile(tmp, b, 0600); err != nil { return fmt.Errorf("router-ca write: %w", err) }
	if err := os.Rename(tmp, s.Path); err != nil { _ = os.Remove(tmp); return fmt.Errorf("router-ca commit: %w", err) }
	return nil
}
