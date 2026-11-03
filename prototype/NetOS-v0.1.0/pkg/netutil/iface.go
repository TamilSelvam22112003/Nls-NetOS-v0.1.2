package netutil
import("context";"fmt";"net")
// DefaultInterface returns the first usable non-loopback interface.
func DefaultInterface(ctx context.Context)(net.Interface,error){if e:=ctx.Err();e!=nil{return net.Interface{},fmt.Errorf("interface discovery: %w",e)};ifs,e:=net.Interfaces();if e!=nil{return net.Interface{},fmt.Errorf("list interfaces: %w",e)};for _,i:=range ifs{if i.Flags&net.FlagLoopback==0&&i.Flags&net.FlagUp!=0{a,e:=i.Addrs();if e==nil&&len(a)>0{return i,nil}}};return net.Interface{},fmt.Errorf("interface discovery: no usable interface")}
