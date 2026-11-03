package enrollment
import("bytes";"context";"fmt";"io";"net/http")
// SCEPRequest models a PKIOperation message.
type SCEPRequest struct{URL string;Message []byte}
// SCEPResponse models the returned CMS payload status.
type SCEPResponse struct{Status int;Message []byte}
// EnrollSCEP sends the PKIOperation transport shape and leaves CMS issuance to a CA adapter.
func EnrollSCEP(ctx context.Context,r SCEPRequest)(SCEPResponse,error){if r.URL==""||len(r.Message)==0{return SCEPResponse{},fmt.Errorf("SCEP URL and message are required")};req,e:=http.NewRequestWithContext(ctx,http.MethodPost,r.URL,bytes.NewReader(r.Message));if e!=nil{return SCEPResponse{},fmt.Errorf("build SCEP request: %w",e)};req.Header.Set("Content-Type","application/x-pki-message");resp,e:=http.DefaultClient.Do(req);if e!=nil{return SCEPResponse{},fmt.Errorf("SCEP request: %w",e)};defer resp.Body.Close();_,_=io.ReadAll(resp.Body);return SCEPResponse{Status:resp.StatusCode},fmt.Errorf("SCEP transport completed: %w",ErrNotImplemented)}
