package netutil
import("context";"fmt";"net")
// ResolveOutbound resolves a host using the caller context.
func ResolveOutbound(ctx context.Context,address string)(string,error){h,p,e:=net.SplitHostPort(address);if e!=nil{return "",fmt.Errorf("split address: %w",e)};ips,e:=net.DefaultResolver.LookupHost(ctx,h);if e!=nil{return "",fmt.Errorf("resolve %s: %w",h,e)};if len(ips)==0{return "",fmt.Errorf("no address for %s",h)};return net.JoinHostPort(ips[0],p),nil}
