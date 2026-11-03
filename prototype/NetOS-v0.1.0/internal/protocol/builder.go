package protocol
import "fmt"
// Build validates and serializes an onboarding message.
func Build(m Message)([]byte,error){if e:=Validate(m);e!=nil{return nil,fmt.Errorf("build packet: %w",e)};b,e:=(Codec{}).Encode(m);if e!=nil{return nil,fmt.Errorf("build packet: %w",e)};return b,nil}
