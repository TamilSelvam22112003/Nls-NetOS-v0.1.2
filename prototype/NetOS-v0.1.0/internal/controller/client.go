package controller
import("context";"crypto/tls";"fmt";"io";"net/http")
// Client retrieves controller configuration over HTTPS.
type Client struct{HTTP *http.Client}
// FetchConfig gets /config from a controller using the supplied context.
func(c Client)FetchConfig(ctx context.Context,address string)([]byte,error){h:=c.HTTP;if h==nil{h=&http.Client{Transport:&http.Transport{TLSClientConfig:&tls.Config{MinVersion:tls.VersionTLS13}}}};r,e:=http.NewRequestWithContext(ctx,http.MethodGet,"https://"+address+"/config",nil);if e!=nil{return nil,fmt.Errorf("controller request: %w",e)};res,e:=h.Do(r);if e!=nil{return nil,fmt.Errorf("controller request: %w",e)};defer res.Body.Close();if res.StatusCode/100!=2{return nil,fmt.Errorf("controller response: %s",res.Status)};b,e:=io.ReadAll(res.Body);if e!=nil{return nil,fmt.Errorf("controller read: %w",e)};return b,nil}
