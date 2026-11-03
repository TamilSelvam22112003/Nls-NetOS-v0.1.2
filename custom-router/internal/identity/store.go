package identity
import("bytes";"crypto/aes";"crypto/cipher";"crypto/rand";"crypto/rsa";"crypto/x509";"encoding/base64";"errors";"fmt";"io";"os";"golang.org/x/crypto/scrypt")
// ErrTPMUnavailable means no hardware TPM adapter is present.
var ErrTPMUnavailable=errors.New("TPM unavailable")
// KeyStore abstracts private-key persistence.
type KeyStore interface{Load()(*rsa.PrivateKey,[]byte,error);Save(*rsa.PrivateKey,[]byte)error}
// TPMStore is the production adapter shape; the lab has no TPM backend.
type TPMStore struct{}
// Load reports TPM absence on the lab host.
func(TPMStore)Load()(*rsa.PrivateKey,[]byte,error){return nil,nil,ErrTPMUnavailable}
// Save reports TPM absence on the lab host.
func(TPMStore)Save(*rsa.PrivateKey,[]byte)error{return ErrTPMUnavailable}
// FileStore encrypts private keys at rest with AES-GCM and a scrypt-derived key.
type FileStore struct{Path,Passphrase string}
func(s FileStore)derive()([]byte,error){if s.Passphrase==""{return nil,fmt.Errorf("empty key-store passphrase")};k,e:=scrypt.Key([]byte(s.Passphrase),[]byte("custom-router-file-store-v1"),32768,8,1,32);if e!=nil{return nil,fmt.Errorf("derive key: %w",e)};return k,nil}
// Save writes AESGCM:<nonce>:<ciphertext> followed by certificate PEM.
func(s FileStore)Save(k *rsa.PrivateKey,cert []byte)error{key,e:=s.derive();if e!=nil{return e};b,e:=aes.NewCipher(key);if e!=nil{return fmt.Errorf("AES: %w",e)};a,e:=cipher.NewGCM(b);if e!=nil{return fmt.Errorf("GCM: %w",e)};n:=make([]byte,a.NonceSize());if _,e=io.ReadFull(rand.Reader,n);e!=nil{return fmt.Errorf("nonce: %w",e)};raw:=x509.MarshalPKCS1PrivateKey(k);ct:=a.Seal(nil,n,raw,cert);head:="AESGCM:"+base64.StdEncoding.EncodeToString(n)+":"+base64.StdEncoding.EncodeToString(ct)+"\n";if e=os.WriteFile(s.Path,append([]byte(head),cert...),0600);e!=nil{return fmt.Errorf("write key store: %w",e)};return nil}
// Load decrypts a FileStore record.
func(s FileStore)Load()(*rsa.PrivateKey,[]byte,error){b,e:=os.ReadFile(s.Path);if e!=nil{return nil,nil,fmt.Errorf("read key store: %w",e)};line,cert,ok:=bytes.Cut(b,[]byte("\n"));if !ok{return nil,nil,fmt.Errorf("invalid key-store record")};parts:=bytes.Split(line,[]byte(":"));if len(parts)!=3||string(parts[0])!="AESGCM"{return nil,nil,fmt.Errorf("invalid AES-GCM header")};n,e:=base64.StdEncoding.DecodeString(string(parts[1]));if e!=nil{return nil,nil,fmt.Errorf("decode nonce: %w",e)};ct,e:=base64.StdEncoding.DecodeString(string(parts[2]));if e!=nil{return nil,nil,fmt.Errorf("decode ciphertext: %w",e)};key,e:=s.derive();if e!=nil{return nil,nil,e};b1,e:=aes.NewCipher(key);if e!=nil{return nil,nil,fmt.Errorf("AES: %w",e)};a,e:=cipher.NewGCM(b1);if e!=nil{return nil,nil,fmt.Errorf("GCM: %w",e)};raw,e:=a.Open(nil,n,ct,cert);if e!=nil{return nil,nil,fmt.Errorf("decrypt private key: %w",e)};k,e:=x509.ParsePKCS1PrivateKey(raw);if e!=nil{return nil,nil,fmt.Errorf("parse private key: %w",e)};return k,cert,nil}
var _ KeyStore=FileStore{}
