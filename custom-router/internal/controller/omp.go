package controller
import("context";"fmt";"net/http";"custom-router/internal/protocol")
// OMPClient represents the lab controller control channel.
type OMPClient struct{HTTP *http.Client}
// Establish performs a context-aware controller probe.
func(o OMPClient)Establish(ctx context.Context,ep protocol.ControllerEndpoint)error{if ep.Role!="controller"{return fmt.Errorf("endpoint is not controller")};if o.HTTP==nil{o.HTTP=http.DefaultClient};req,e:=http.NewRequestWithContext(ctx,http.MethodHead,ep.Address,nil);if e!=nil{return fmt.Errorf("build controller probe: %w",e)};resp,e:=o.HTTP.Do(req);if e!=nil{return fmt.Errorf("controller probe: %w",e)};defer resp.Body.Close();if resp.StatusCode>=400{return fmt.Errorf("controller probe failed: %s",resp.Status)};return nil}
