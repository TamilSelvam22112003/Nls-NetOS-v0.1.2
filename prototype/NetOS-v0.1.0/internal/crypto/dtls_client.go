package crypto

import("context";"crypto/tls";"crypto/x509";"fmt";"net";"os";"github.com/pion/dtls/v2")
// DTLSClient establishes the encrypted validator transport.
type DTLSClient struct{RootCAPath string;ClientCert tls.Certificate;Organization string}
// Dial performs DTLS setup, then verifies the server certificate chain and organization; failure closes the connection.
func(c DTLSClient)Dial(ctx context.Context,address string)(net.Conn,error){b,e:=os.ReadFile(c.RootCAPath);if e!=nil{return nil,fmt.Errorf("read DTLS root CA: %w",e)};roots:=x509.NewCertPool();if !roots.AppendCertsFromPEM(b){return nil,fmt.Errorf("parse DTLS root CA")};raw,e:=(&net.Dialer{}).DialContext(ctx,"udp",address);if e!=nil{return nil,fmt.Errorf("dial validator: %w",e)};cfg:=&dtls.Config{Certificates:[]tls.Certificate{c.ClientCert},RootCAs:roots,InsecureSkipVerify:true,ExtendedMasterSecret:dtls.RequireExtendedMasterSecret};conn,e:=dtls.Client(raw,cfg);if e!=nil{_ = raw.Close();return nil,fmt.Errorf("DTLS client: %w",e)};if e=conn.HandshakeContext(ctx);e!=nil{_ = conn.Close();return nil,fmt.Errorf("DTLS handshake: %w",e)};if e=VerifyServer(conn.ConnectionState().PeerCertificates,c.RootCAPath,c.Organization);e!=nil{_ = conn.Close();return nil,fmt.Errorf("verify validator: %w",e)};return conn,nil}
