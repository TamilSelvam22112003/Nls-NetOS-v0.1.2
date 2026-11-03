package identity
import("crypto/x509";"encoding/pem";"fmt";"os")
// BoardID is a parsed device identity certificate.
type BoardID struct{Certificate *x509.Certificate;PEM []byte}
// LoadBoardID loads a PEM board identity certificate.
func LoadBoardID(path string)(BoardID,error){b,e:=os.ReadFile(path);if e!=nil{return BoardID{},fmt.Errorf("read board certificate: %w",e)};bl,_:=pem.Decode(b);if bl==nil{return BoardID{},fmt.Errorf("decode board certificate")};c,e:=x509.ParseCertificate(bl.Bytes);if e!=nil{return BoardID{},fmt.Errorf("parse board certificate: %w",e)};return BoardID{c,b},nil}
