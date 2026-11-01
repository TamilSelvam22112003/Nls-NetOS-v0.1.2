CREATE TABLE IF NOT EXISTS router_ca_synchronization (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    router_ca_id BIGINT UNSIGNED NOT NULL,
    sync_type ENUM('provider','certificate','trust','key_state','metadata','full') NOT NULL,
    direction ENUM('pull','push','bidirectional') NOT NULL,
    requested_at DATETIME NULL,
    completed_at DATETIME NULL,
    next_attempt_at DATETIME NULL,
    attempt_count INT UNSIGNED NOT NULL DEFAULT 0,
    status ENUM('pending','running','success','failed','expired','blocked') NOT NULL DEFAULT 'pending',
    last_error_code VARCHAR(128) NULL,
    last_error_message VARCHAR(1024) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_router_ca_sync_due (next_attempt_at, status),
    CONSTRAINT fk_router_ca_sync_ca FOREIGN KEY (router_ca_id) REFERENCES router_ca(id)
) ENGINE=InnoDB;
