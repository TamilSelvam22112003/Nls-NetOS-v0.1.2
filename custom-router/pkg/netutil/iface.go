package netutil
import("context";"fmt";"net")
// DefaultInterface returns an active non-loopback interface.
func DefaultInterface(ctx context.Context)(string,error){select{case<-ctx.Done():return "",ctx.Err();default:};ifs,e:=net.Interfaces();if e!=nil{return "",fmt.Errorf("list interfaces: %w",e)};for _,i:=range ifs{if i.Flags&net.FlagLoopback!=0||i.Flags&net.FlagUp==0{continue};a,e:=i.Addrs();if e==nil&&len(a)>0{return i.Name,nil}};return "",fmt.Errorf("no active non-loopback interface")}
