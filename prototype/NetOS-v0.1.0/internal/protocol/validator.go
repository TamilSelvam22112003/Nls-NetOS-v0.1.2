package protocol
import "fmt"
// Validate checks structural rules of onboarding messages.
func Validate(m Message)error{if m.Type< MessageHello||m.Type>MessageError{return fmt.Errorf("unknown message type %d",m.Type)};if m.Fields==nil{return fmt.Errorf("message fields are nil")};if m.Type==MessageChallenge&&len(m.Fields[FieldNonce])!=32{return fmt.Errorf("challenge nonce must be 32 bytes")};if m.Type==MessageResponse{for _,k:=range []TLVType{FieldSignature,FieldSerial,FieldChassis,FieldBoardCert}{if len(m.Fields[k])==0{return fmt.Errorf("required response field %d missing",k)}}};if m.Type==MessageControllers&&len(m.Fields[FieldControllers])==0{return fmt.Errorf("controller list missing")};return nil}
