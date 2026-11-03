package identity
import("crypto/rand";"crypto/rsa";"fmt")
// GenerateRSA generates an RSA private key of at least 2048 bits.
func GenerateRSA(bits int)(*rsa.PrivateKey,error){if bits<2048{return nil,fmt.Errorf("RSA size %d is below 2048",bits)};k,e:=rsa.GenerateKey(rand.Reader,bits);if e!=nil{return nil,fmt.Errorf("generate RSA key: %w",e)};return k,nil}
