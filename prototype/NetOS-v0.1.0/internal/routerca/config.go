package routerca

import "time"

// Config is the persistent Router-CA onboarding policy used by the lab router.
type Config struct {
	Enabled             bool     `json:"enabled"`
	AutoEnroll          bool     `json:"auto_enroll"`
	ValidatorAddresses  []string `json:"validator_addresses"`
	Organization        string   `json:"organization"`
	RootCA              string   `json:"root_ca"`
	IdentityStore       string   `json:"identity_store"`
	IdentityPassphrase  string   `json:"identity_passphrase_env"`
	Serial              string   `json:"serial"`
	Chassis             string   `json:"chassis"`
	BoardID             string   `json:"board_id"`
	RetryInitial        time.Duration `json:"-"`
	RetryMax            time.Duration `json:"-"`
}

// DefaultConfig returns safe lab defaults. Router-CA is disabled until explicitly enabled.
func DefaultConfig() Config {
	return Config{Enabled: false, AutoEnroll: true, RetryInitial: 250 * time.Millisecond, RetryMax: 10 * time.Second}
}
