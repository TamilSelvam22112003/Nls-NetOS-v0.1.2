package protocol
import("context";"crypto";"crypto/rsa";"crypto/sha256";"crypto/x509";"fmt";"io";"time";ncrypto "custom-router/internal/crypto")
// Handshaker drives the Validator challenge/response exchange.
type Handshaker interface{Run(context.Context,io.ReadWriter)error}
// ClientHandshaker is the router side of the exchange.
type ClientHandshaker struct{PrivateKey *rsa.PrivateKey;Serial,Chassis string;BoardIDCertificate []byte}
// Run receives a 256-bit challenge and returns the signed identity.
func(h ClientHandshaker)Run(ctx context.Context,rw io.ReadWriter)error{select{case<-ctx.Done():return ctx.Err();default:};c:=NewCodec(rw);var ch Challenge;t,e:=c.Read(&ch);if e!=nil{return fmt.Errorf("read challenge: %w",e)};if t!=MsgChallenge{return fmt.Errorf("expected challenge, got %d",t)};r,e:=ncrypto.SignChallenge(h.PrivateKey,ch.Nonce,h.Serial,h.Chassis,h.BoardIDCertificate);if e!=nil{return e};if e=Write(rw,MsgChallengeResponse,ChallengeResponse{r.Signature,r.Serial,r.Chassis,r.BoardIDCertificate});e!=nil{return fmt.Errorf("send response: %w",e)};return nil}
// VerifyChallengeSignature verifies certificate validity and RSA-PSS proof.
func VerifyChallengeSignature(certDER,nonce,sig []byte)error{c,e:=x509.ParseCertificate(certDER);if e!=nil{return fmt.Errorf("parse board certificate: %w",e)};if e=c.CheckValidity(time.Now());e!=nil{return fmt.Errorf("board certificate validity: %w",e)};pub,ok:=c.PublicKey.(*rsa.PublicKey);if !ok{return fmt.Errorf("board certificate is not RSA")};h:=sha256.Sum256(nonce);if e=rsa.VerifyPSS(pub,crypto.SHA256,h[:],sig,&rsa.PSSOptions{SaltLength:32,Hash:crypto.SHA256});e!=nil{return fmt.Errorf("verify challenge signature: %w",e)};return nil}
