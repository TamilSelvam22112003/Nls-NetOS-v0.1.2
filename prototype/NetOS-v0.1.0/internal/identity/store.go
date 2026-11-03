package identity

import("crypto/aes";"crypto/cipher";"crypto/rand";"crypto/rsa";"crypto/x509";"encoding/base64";"errors";"fmt";"io";"os";"path/filepath";"golang.org/x/crypto/scrypt")
// ErrTPMUnavailable indicates that no usable TPM backend is connected.
var ErrTPMUnavailable=errors.New("TPM unavailable")
// KeyStore abstracts protected private-key persistence.
type KeyStore interface{Load()(*rsa.PrivateKey,[]byte,error);Save(*rsa.PrivateKey,[]byte)error}
// TPMStore is the production interface shape for a TPM-backed implementation.
type TPMStore struct{}
// Load reports TPM unavailability in this host-independent prototype.
func(TPMStore)Load()(*rsa.PrivateKey,[]byte,error){return nil,nil,ErrTPMUnavailable}
// Save reports TPM unavailability in this host-independent prototype.
func(TPMStore)Save(*rsa.PrivateKey,[]byte)error{return ErrTPMUnavailable}
// FileStore encrypts private-key material at rest using AES-GCM and scrypt.
type FileStore struct{Path,Passphrase string}
// Load decrypts an AESGCM:<base64> store.
func(s FileStore)Load()(*rsa.PrivateKey,[]byte,error){b,e:=os.ReadFile(s.Path);if e!=nil{return nil,nil,fmt.Errorf("read key store: %w",e)};if len(b)<7||string(b[:7])!="AESGCM:"{return nil,nil,fmt.Errorf("key store: invalid format")};raw,e:=base64.StdEncoding.DecodeString(string(b[7:]));if e!=nil{return nil,nil,fmt.Errorf("key store base64: %w",e)};if len(raw)<28{return nil,nil,fmt.Errorf("key store: short ciphertext")};k,e:=scrypt.Key([]byte(s.Passphrase),raw[:16],32768,8,1,32);if e!=nil{return nil,nil,fmt.Errorf("scrypt: %w",e)};block,e:=aes.NewCipher(k);if e!=nil{return nil,nil,fmt.Errorf("AES: %w",e)};a,e:=cipher.NewGCM(block);if e!=nil{return nil,nil,fmt.Errorf("GCM: %w",e)};p,e:=a.Open(nil,raw[16:28],raw[28:],nil);if e!=nil{return nil,nil,fmt.Errorf("decrypt key store: %w",e)};i:=-1;for n,v:=range p{if v==0{i=n;break}};if i<=0{return nil,nil,fmt.Errorf("key store: malformed payload")};key,e:=x509.ParsePKCS1PrivateKey(p[:i]);if e!=nil{return nil,nil,fmt.Errorf("parse private key: %w",e)};return key,append([]byte(nil),p[i+1:]...),nil}
// Save encrypts an RSA private key and certificate with AES-GCM using a scrypt-derived 256-bit key.
func(s FileStore)Save(key *rsa.PrivateKey,cert []byte)error{if key==nil{return fmt.Errorf("save key store: nil private key")};if e:=os.MkdirAll(filepath.Dir(s.Path),0700);e!=nil{return fmt.Errorf("create key store directory: %w",e)};salt:=make([]byte,16);nonce:=make([]byte,12);if _,e:=io.ReadFull(rand.Reader,salt);e!=nil{return fmt.Errorf("salt: %w",e)};if _,e:=io.ReadFull(rand.Reader,nonce);e!=nil{return fmt.Errorf("nonce: %w",e)};k,e:=scrypt.Key([]byte(s.Passphrase),salt,32768,8,1,32);if e!=nil{return fmt.Errorf("scrypt: %w",e)};block,e:=aes.NewCipher(k);if e!=nil{return fmt.Errorf("AES: %w",e)};a,e:=cipher.NewGCM(block);if e!=nil{return fmt.Errorf("GCM: %w",e)};p:=append(x509.MarshalPKCS1PrivateKey(key),0);p=append(p,cert...);ct:=a.Seal(nil,nonce,p,nil);raw:=append(append(append([]byte{},salt...),nonce...),ct...);if e:=os.WriteFile(s.Path,[]byte("AESGCM:"+base64.StdEncoding.EncodeToString(raw)),0600);e!=nil{return fmt.Errorf("write key store: %w",e)};return nil}
