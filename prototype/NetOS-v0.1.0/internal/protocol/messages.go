package protocol

// MessageType identifies an onboarding message.
type MessageType uint8
const(MessageHello MessageType=1;MessageChallenge MessageType=2;MessageResponse MessageType=3;MessageControllers MessageType=4;MessageError MessageType=5)
// TLVType identifies a message field.
type TLVType uint16
const(FieldNonce TLVType=1;FieldSerial TLVType=2;FieldChassis TLVType=3;FieldBoardCert TLVType=4;FieldSignature TLVType=5;FieldControllers TLVType=6;FieldError TLVType=7)
// Message is the logical onboarding message.
type Message struct{Type MessageType;Fields map[TLVType][]byte}
// ControllerEndpoint describes a controller or manager endpoint.
type ControllerEndpoint struct{Role,Address string}
