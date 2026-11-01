-- Populate only non-secret provider metadata here.
-- Real provider endpoints, trust anchors and fingerprints must be verified before production use.
INSERT INTO router_ca_provider
(provider_name, provider_type, organization, country_code, recommended, priority, status)
VALUES
('MANUFACTURER-CA', 'manufacturer', 'Manufacturer', NULL, TRUE, 10, 'unknown'),
('ISP-CA', 'isp', 'ISP', NULL, TRUE, 20, 'unknown'),
('PUBLIC-CA', 'public', 'Public CA', NULL, TRUE, 30, 'unknown')
ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP;
