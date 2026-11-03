package validator
import("context";"crypto/rsa";"crypto/tls";"encoding/pem";"fmt";"io";"time";"custom-router/config";ncrypto "custom-router/internal/crypto";"custom-router/internal/protocol")
// Client performs DTLS connection and router authentication.
type Client struct{Config config.Config;PrivateKey *rsa.PrivateKey;BoardIDCertificate []byte;Timeout time.Duration}
// Connect establishes DTLS and runs the challenge-response exchange.
func(c Client)Connect(ctx context.Context,address string)(io.ReadWriteCloser,error){bl,_:=pem.Decode(c.BoardIDCertificate);if bl==nil{return nil,fmt.Errorf("invalid board certificate PEM")};cert:=tls.Certificate{Certificate:[][]byte{bl.Bytes},PrivateKey:c.PrivateKey};dc:=ncrypto.DTLSClient{RootCAPath:c.Config.RootCA,Organization:c.Config.OrganizationName,Certificate:cert,Timeout:c.Timeout};conn,e:=dc.Dial(ctx,address);if e!=nil{return nil,e};hs:=protocol.ClientHandshaker{PrivateKey:c.PrivateKey,Serial:c.Config.Serial,Chassis:c.Config.Chassis,BoardIDCertificate:c.BoardIDCertificate};if e=hs.Run(ctx,conn);e!=nil{conn.Close();return nil,fmt.Errorf("authentication: %w",e)};return conn,nil}
