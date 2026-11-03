package crypto

import("crypto";"crypto/rand";"crypto/rsa";"crypto/sha256";"crypto/x509";"encoding/pem";"fmt";"os";"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/protocol")

// Signer signs validator nonces with RSA-PSS-SHA256 and returns router identity data.
type Signer struct{PrivateKey *rsa.PrivateKey;Serial,Chassis,BoardCertificate string}
// SignChallenge signs exactly a 256-bit validator nonce.
func(s Signer)SignChallenge(nonce []byte)(protocol.SignedChallenge,error){if len(nonce)!=32{return protocol.SignedChallenge{},fmt.Errorf("sign challenge: nonce must be 32 bytes")};if s.PrivateKey==nil{return protocol.SignedChallenge{},fmt.Errorf("sign challenge: private key is nil")};h:=sha256.Sum256(nonce);sig,e:=rsa.SignPSS(rand.Reader,s.PrivateKey,crypto.SHA256,h[:],&rsa.PSSOptions{SaltLength:32,Hash:crypto.SHA256});if e!=nil{return protocol.SignedChallenge{},fmt.Errorf("sign nonce: %w",e)};return protocol.SignedChallenge{Signature:sig,Serial:[]byte(s.Serial),Chassis:[]byte(s.Chassis),BoardCertificate:[]byte(s.BoardCertificate)},nil}
// LoadBoardCertificate loads a PEM board certificate.
func LoadBoardCertificate(path string)(*x509.Certificate,error){b,e:=os.ReadFile(path);if e!=nil{return nil,fmt.Errorf("read board certificate: %w",e)};p,_:=pem.Decode(b);if p==nil{return nil,fmt.Errorf("decode board certificate: invalid PEM")};c,e:=x509.ParseCertificate(p.Bytes);if e!=nil{return nil,fmt.Errorf("parse board certificate: %w",e)};return c,nil}
