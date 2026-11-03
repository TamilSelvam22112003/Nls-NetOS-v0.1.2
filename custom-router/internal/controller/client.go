package controller
import("context";"fmt";"net/http";"time";"custom-router/internal/protocol")
// Client probes discovered controller endpoints.
type Client struct{HTTP *http.Client;Timeout time.Duration}
// Connect establishes the lab controller session.
func(c Client)Connect(ctx context.Context,eps []protocol.ControllerEndpoint)error{if c.HTTP==nil{c.HTTP=&http.Client{Timeout:c.Timeout}};for _,ep:=range eps{if ep.Role!="controller"{continue};req,e:=http.NewRequestWithContext(ctx,http.MethodHead,ep.Address,nil);if e!=nil{return fmt.Errorf("controller request: %w",e)};resp,e:=c.HTTP.Do(req);if e!=nil{return fmt.Errorf("controller connect: %w",e)};resp.Body.Close();if resp.StatusCode>=500{return fmt.Errorf("controller returned %s",resp.Status)}};return nil}
