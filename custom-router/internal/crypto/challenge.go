package crypto
import("crypto";"crypto/rand";"crypto/rsa";"crypto/sha256";"fmt")
// ChallengeResponse is the signed router identity response.
type ChallengeResponse struct{Signature []byte;Serial string;Chassis string;BoardIDCertificate []byte}
// SignChallenge signs a 256-bit nonce using RSA-PSS/SHA-256.
func SignChallenge(key *rsa.PrivateKey,nonce []byte,serial,chassis string,cert []byte)(ChallengeResponse,error){if len(nonce)!=32{return ChallengeResponse{},fmt.Errorf("challenge must be exactly 256 bits")};h:=sha256.Sum256(nonce);sig,e:=rsa.SignPSS(rand.Reader,key,crypto.SHA256,h[:],&rsa.PSSOptions{SaltLength:32,Hash:crypto.SHA256});if e!=nil{return ChallengeResponse{},fmt.Errorf("sign challenge: %w",e)};return ChallengeResponse{sig,serial,chassis,cert},nil}
