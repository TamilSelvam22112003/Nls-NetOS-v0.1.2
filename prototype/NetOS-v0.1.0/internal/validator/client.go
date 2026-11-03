package validator

import("context";"fmt";"net";"time";"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/crypto";"github.com/TamilSelvam22112003/Nls-NetOS-v0.1.2/prototype/NetOS-v0.1.0/internal/protocol")
// Client connects to the Validator and runs application mutual authentication.
type Client struct{DTLS crypto.DTLSClient;Handshaker protocol.Handshaker;Timeout time.Duration}
// Connect establishes DTLS, runs challenge/response, and returns the validated controller message.
func(c Client)Connect(ctx context.Context,address string)(net.Conn,protocol.Message,error){d:=c.Timeout;if d<=0{d=10*time.Second};cc,cancel:=context.WithTimeout(ctx,d);defer cancel();conn,e:=c.DTLS.Dial(cc,address);if e!=nil{return nil,protocol.Message{},fmt.Errorf("validator connect: %w",e)};m,e:=c.Handshaker.Run(cc,conn);if e!=nil{_ = conn.Close();return nil,protocol.Message{},fmt.Errorf("validator authentication: %w",e)};return conn,m,nil}
