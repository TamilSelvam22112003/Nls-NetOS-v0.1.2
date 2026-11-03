package identity

import("crypto/rand";"crypto/rsa";"crypto/x509";"crypto/x509/pkix";"encoding/pem";"fmt";"math/big";"time")
// Identity contains the router private key and board-ID certificate.
type Identity struct{PrivateKey *rsa.PrivateKey;CertificatePEM []byte}
// Generate creates a 3072-bit RSA identity and self-signed board certificate for first boot.
func Generate(serial,chassis,board string)(Identity,error){k,e:=rsa.GenerateKey(rand.Reader,3072);if e!=nil{return Identity{},fmt.Errorf("generate identity: %w",e)};n,e:=rand.Int(rand.Reader,new(big.Int).Lsh(big.NewInt(1),128));if e!=nil{return Identity{},fmt.Errorf("identity serial: %w",e)};now:=time.Now().UTC();t:=&x509.Certificate{SerialNumber:n,Subject:pkix.Name{CommonName:"NetOS Board ID",Organization:[]string{"NetOS"},OrganizationalUnit:[]string{board},SerialNumber:serial},NotBefore:now.Add(-time.Minute),NotAfter:now.Add(365*24*time.Hour),KeyUsage:x509.KeyUsageDigitalSignature|x509.KeyUsageKeyEncipherment,ExtKeyUsage:[]x509.ExtKeyUsage{x509.ExtKeyUsageClientAuth},BasicConstraintsValid:true};der,e:=x509.CreateCertificate(rand.Reader,t,t,&k.PublicKey,k);if e!=nil{return Identity{},fmt.Errorf("create board certificate: %w",e)};return Identity{k,pem.EncodeToMemory(&pem.Block{Type:"CERTIFICATE",Bytes:der})},nil}
