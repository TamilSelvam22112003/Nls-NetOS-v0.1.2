package protocol

import("context";"fmt";"net")

// Handshaker runs the application challenge/response protocol over an established connection.
type Handshaker interface{Run(context.Context,net.Conn)(Message,error)}
// SignedChallenge is the router identity proof returned to the validator.
type SignedChallenge struct{Signature,Serial,Chassis,BoardCertificate []byte}
// ChallengeSigner signs validator nonces.
type ChallengeSigner interface{SignChallenge([]byte)(SignedChallenge,error)}
// ClientHandshaker implements the validator challenge exchange.
type ClientHandshaker struct{Codec Codec;Signer ChallengeSigner}
// Run receives a 32-byte nonce, returns its RSA-PSS proof and identity, then receives controller addresses.
func(h ClientHandshaker)Run(ctx context.Context,c net.Conn)(Message,error){if h.Signer==nil{return Message{},fmt.Errorf("handshake: signer is nil")};if d,ok:=ctx.Deadline();ok{if err:=c.SetDeadline(d);err!=nil{return Message{},fmt.Errorf("handshake deadline: %w",err)}};m,e:=h.Codec.Decode(c);if e!=nil{return Message{},fmt.Errorf("receive challenge: %w",e)};if m.Type!=MessageChallenge{return Message{},fmt.Errorf("unexpected message type %d",m.Type)};n:=m.Fields[FieldNonce];if len(n)!=32{return Message{},fmt.Errorf("challenge nonce must be 256 bits")};s,e:=h.Signer.SignChallenge(n);if e!=nil{return Message{},fmt.Errorf("sign challenge: %w",e)};b,e:=h.Codec.Encode(Message{Type:MessageResponse,Fields:map[TLVType][]byte{FieldSignature:s.Signature,FieldSerial:s.Serial,FieldChassis:s.Chassis,FieldBoardCert:s.BoardCertificate}});if e!=nil{return Message{},fmt.Errorf("encode response: %w",e)};for len(b)>0{select{case<-ctx.Done():return Message{},fmt.Errorf("send response: %w",ctx.Err());default:};n,e:=c.Write(b);if e!=nil{return Message{},fmt.Errorf("send response: %w",e)};b=b[n:]};m,e=h.Codec.Decode(c);if e!=nil{return Message{},fmt.Errorf("receive controller list: %w",e)};if m.Type==MessageError{return Message{},fmt.Errorf("validator rejected router: %s",m.Fields[FieldError])};if m.Type!=MessageControllers{return Message{},fmt.Errorf("expected controller list")};return m,nil}
