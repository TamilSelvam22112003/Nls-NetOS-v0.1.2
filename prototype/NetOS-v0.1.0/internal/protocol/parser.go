package protocol
import("bytes";"fmt")
// Parse decodes one complete framed onboarding message.
func Parse(data []byte)(Message,error){m,e:=(Codec{}).Decode(bytes.NewReader(data));if e!=nil{return Message{},fmt.Errorf("parse packet: %w",e)};return m,nil}
