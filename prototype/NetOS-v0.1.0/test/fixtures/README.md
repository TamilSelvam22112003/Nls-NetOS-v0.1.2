# Fixtures

`root-ca.pem` and `device-boardid.pem` are test certificates. The matching private key is intentionally documented only in the repository README as test material; never use it in production. `device-boardid.key.enc` is a placeholder using the FileStore format `AESGCM:<base64(salt||nonce||ciphertext)>`; generate it with FileStore and a test passphrase before an integration run.
