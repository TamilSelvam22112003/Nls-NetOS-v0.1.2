package routerca

import (
	"context"
	"fmt"
	"sync"
)

// Onboarder starts the real onboarding state machine when Router-CA is enabled.
type Onboarder interface { Run(context.Context, Config) error }

// Service owns persistent enable/disable state and cancels active onboarding when disabled.
type Service struct {
	Store *Store
	Onboarder Onboarder
	mu sync.Mutex
	cancel context.CancelFunc
}

// SetEnabled persists the desired state and immediately starts/stops runtime onboarding.
func (s *Service) SetEnabled(parent context.Context, enabled bool) error {
	s.mu.Lock(); defer s.mu.Unlock()
	cfg, err := s.Store.Load(); if err != nil { return err }
	cfg.Enabled = enabled
	if err := s.Store.Save(cfg); err != nil { return err }
	if !enabled {
		if s.cancel != nil { s.cancel(); s.cancel = nil }
		return nil
	}
	if s.Onboarder == nil { return fmt.Errorf("router-ca onboarder is not configured") }
	if s.cancel != nil { s.cancel(); s.cancel = nil }
	ctx, cancel := context.WithCancel(parent); s.cancel = cancel
	go func() {
		err := s.Onboarder.Run(ctx, cfg)
		s.mu.Lock(); defer s.mu.Unlock()
		if s.cancel == cancel { s.cancel = nil }
		_ = err
	}()
	return nil
}

// Boot evaluates persistent configuration and starts onboarding only when enabled.
func (s *Service) Boot(parent context.Context) error {
	cfg, err := s.Store.Load(); if err != nil { return err }
	if !cfg.Enabled { return nil }
	return s.SetEnabled(parent, true)
}

// Disable is equivalent to the network engineer's router-ca disable command.
func (s *Service) Disable() error { return s.SetEnabled(context.Background(), false) }
