package manager
import("context";"fmt";"io";"net/http";"time";"custom-router/internal/protocol")
// Client fetches configuration from a discovered manager.
type Client struct{HTTP *http.Client;Timeout time.Duration}
// Fetch gets /config from the first manager endpoint.
func(c Client)Fetch(ctx context.Context,eps []protocol.ControllerEndpoint)([]byte,error){if c.HTTP==nil{c.HTTP=&http.Client{Timeout:c.Timeout}};for _,ep:=range eps{if ep.Role!="manager"{continue};req,e:=http.NewRequestWithContext(ctx,http.MethodGet,ep.Address+"/config",nil);if e!=nil{return nil,fmt.Errorf("manager request: %w",e)};resp,e:=c.HTTP.Do(req);if e!=nil{return nil,fmt.Errorf("manager connect: %w",e)};b,er:=io.ReadAll(resp.Body);resp.Body.Close();if er!=nil{return nil,fmt.Errorf("read manager config: %w",er)};if resp.StatusCode>=400{return nil,fmt.Errorf("manager returned %s",resp.Status)};return b,nil};return nil,fmt.Errorf("no manager endpoint")}
