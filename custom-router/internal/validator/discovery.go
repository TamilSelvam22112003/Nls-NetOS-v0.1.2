package validator
import("context";"fmt";"io";"custom-router/internal/protocol")
// Discover decodes the controller/manager list returned after authentication.
func Discover(ctx context.Context,r io.Reader)([]protocol.ControllerEndpoint,error){select{case<-ctx.Done():return nil,ctx.Err();default:};var l protocol.ControllerList;t,e:=protocol.NewCodec(r).Read(&l);if e!=nil{return nil,fmt.Errorf("decode discovery: %w",e)};if t!=protocol.MsgControllerList{return nil,fmt.Errorf("unexpected discovery type %d",t)};return l.Endpoints,nil}
