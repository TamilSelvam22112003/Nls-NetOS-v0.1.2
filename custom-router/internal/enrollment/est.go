package enrollment
import("context";"encoding/base64";"fmt";"io";"net/http";"strings")
// ErrNotImplemented indicates transport is present but CA issuance policy is not enabled.
var ErrNotImplemented=fmt.Errorf("certificate issuance not implemented")
// ESTRequest models RFC 7030 simpleenroll input.
type ESTRequest struct{URL string;CSRDER []byte}
// ESTResponse models the HTTP result.
type ESTResponse struct{Status int;CertificateDER []byte}
// EnrollEST sends the simpleenroll request shape and leaves issuance to the CA adapter.
func EnrollEST(ctx context.Context,r ESTRequest)(ESTResponse,error){if r.URL==""||len(r.CSRDER)==0{return ESTResponse{},fmt.Errorf("EST URL and CSR are required")};req,e:=http.NewRequestWithContext(ctx,http.MethodPost,r.URL,strings.NewReader(base64.StdEncoding.EncodeToString(r.CSRDER)));if e!=nil{return ESTResponse{},fmt.Errorf("build EST request: %w",e)};req.Header.Set("Content-Type","application/pkcs10");resp,e:=http.DefaultClient.Do(req);if e!=nil{return ESTResponse{},fmt.Errorf("EST request: %w",e)};defer resp.Body.Close();_,_=io.ReadAll(resp.Body);return ESTResponse{Status:resp.StatusCode},fmt.Errorf("EST transport completed: %w",ErrNotImplemented)}
