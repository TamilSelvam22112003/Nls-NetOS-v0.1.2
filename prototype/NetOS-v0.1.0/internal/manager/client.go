package manager
import("context";"fmt";"io";"net/http")
// Client retrieves manager configuration over HTTPS.
type Client struct{HTTP *http.Client}
// Fetch gets /config from a manager using the supplied context.
func(c Client)Fetch(ctx context.Context,address string)([]byte,error){h:=c.HTTP;if h==nil{h=http.DefaultClient};r,e:=http.NewRequestWithContext(ctx,http.MethodGet,"https://"+address+"/config",nil);if e!=nil{return nil,fmt.Errorf("manager request: %w",e)};res,e:=h.Do(r);if e!=nil{return nil,fmt.Errorf("manager request: %w",e)};defer res.Body.Close();if res.StatusCode/100!=2{return nil,fmt.Errorf("manager response: %s",res.Status)};b,e:=io.ReadAll(res.Body);if e!=nil{return nil,fmt.Errorf("manager read: %w",e)};return b,nil}
