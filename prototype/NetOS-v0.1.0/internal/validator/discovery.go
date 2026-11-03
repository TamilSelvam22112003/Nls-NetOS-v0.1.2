package validator
import("fmt";"strings";"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/protocol")
// Discover decodes the controller/manager list returned by the Validator.
func Discover(m protocol.Message)([]protocol.ControllerEndpoint,error){b:=m.Fields[protocol.FieldControllers];if len(b)==0{return nil,fmt.Errorf("controller discovery: empty list")};var out []protocol.ControllerEndpoint;for _,line:=range strings.Split(strings.TrimSpace(string(b)),"\n"){p:=strings.SplitN(strings.TrimSpace(line),"=",2);if len(p)!=2||p[0]==""||p[1]==""{return nil,fmt.Errorf("controller discovery: malformed endpoint %q",line)};out=append(out,protocol.ControllerEndpoint{Role:p[0],Address:p[1]})};return out,nil}
