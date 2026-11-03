package enrollment
import("context";"crypto/x509";"encoding/base64";"fmt";"net/http";"strings")
// ErrNotImplemented marks an intentionally incomplete external enrollment operation.
var ErrNotImplemented=fmt.Errorf("not implemented")
// ESTRequest represents RFC 7030 simpleenroll input.
type ESTRequest struct{CSRDER []byte}
// ESTClient is an EST enrollment protocol boundary.
type ESTClient struct{HTTP *http.Client;Endpoint string}
// SimpleEnroll constructs the RFC 7030 /simpleenroll POST with base64 DER CSR and returns ErrNotImplemented after request construction.
func(c ESTClient)SimpleEnroll(ctx context.Context,csr *x509.CertificateRequest)([]byte,error){if csr==nil{return nil,fmt.Errorf("EST: nil CSR")};if c.Endpoint==""{return nil,fmt.Errorf("EST: empty endpoint")};body:=base64.StdEncoding.EncodeToString(csr.Raw);req,e:=http.NewRequestWithContext(ctx,http.MethodPost,strings.TrimRight(c.Endpoint,"/")+"/simpleenroll",strings.NewReader(body));if e!=nil{return nil,fmt.Errorf("EST request: %w",e)};req.Header.Set("Content-Type","application/pkcs10");return nil,fmt.Errorf("EST simpleenroll: %w",ErrNotImplemented)}
