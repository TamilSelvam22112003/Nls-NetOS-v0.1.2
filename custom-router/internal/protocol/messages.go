package protocol
// MessageType identifies a lab handshake TLV.
type MessageType uint16
const(MsgChallenge MessageType=1;MsgChallengeResponse MessageType=2;MsgControllerList MessageType=3;MsgError MessageType=4)
// Challenge is the Validator nonce.
type Challenge struct{Nonce []byte `json:"nonce"`}
// ChallengeResponse contains router proof and identity.
type ChallengeResponse struct{Signature []byte `json:"signature"`;Serial string `json:"serial"`;Chassis string `json:"chassis"`;BoardIDCertificate []byte `json:"board_id_certificate"`}
// ControllerEndpoint identifies a controller or manager.
type ControllerEndpoint struct{Role string `json:"role"`;Address string `json:"address"`}
// ControllerList is returned after authentication.
type ControllerList struct{Endpoints []ControllerEndpoint `json:"endpoints"`}
// ErrorMessage describes an authentication failure.
type ErrorMessage struct{Code string `json:"code"`;Detail string `json:"detail"`}
