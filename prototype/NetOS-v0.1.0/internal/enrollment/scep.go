package enrollment
import("context";"fmt";"net/http")
// SCEPRequest represents PKIOperation input.
type SCEPRequest struct{Message []byte;URL string}
// SCEPClient is a SCEP enrollment protocol boundary.
type SCEPClient struct{HTTP *http.Client}
// PKIOperation validates the request and constructs the POST boundary before returning ErrNotImplemented.
func(c SCEPClient)PKIOperation(ctx context.Context,r SCEPRequest)([]byte,error){if r.URL==""||len(r.Message)==0{return nil,fmt.Errorf("SCEP PKIOperation: invalid request")};req,e:=http.NewRequestWithContext(ctx,http.MethodPost,r.URL,nil);if e!=nil{return nil,fmt.Errorf("SCEP request: %w",e)};req.Header.Set("Content-Type","application/x-pki-message");return nil,fmt.Errorf("SCEP PKIOperation: %w",ErrNotImplemented)}
