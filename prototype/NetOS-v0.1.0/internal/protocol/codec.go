package protocol

import("bytes";"encoding/binary";"fmt";"io")

// Codec implements uint32 frame length + uint8 type + repeated uint16 TLV type/uint32 TLV length/value, network byte order.
type Codec struct{}
// Encode serializes one message.
func(Codec)Encode(m Message)([]byte,error){var b bytes.Buffer;b.WriteByte(byte(m.Type));for k,v:=range m.Fields{if err:=binary.Write(&b,binary.BigEndian,uint16(k));err!=nil{return nil,fmt.Errorf("encode type: %w",err)};if err:=binary.Write(&b,binary.BigEndian,uint32(len(v)));err!=nil{return nil,fmt.Errorf("encode length: %w",err)};b.Write(v)};var out bytes.Buffer;if err:=binary.Write(&out,binary.BigEndian,uint32(b.Len()));err!=nil{return nil,fmt.Errorf("encode frame: %w",err)};out.Write(b.Bytes());return out.Bytes(),nil}
// Decode reads one framed message.
func(Codec)Decode(r io.Reader)(Message,error){var n uint32;if err:=binary.Read(r,binary.BigEndian,&n);err!=nil{return Message{},fmt.Errorf("decode frame length: %w",err)};if n<1||n>1<<20{return Message{},fmt.Errorf("decode frame length %d",n)};b:=make([]byte,n);if _,err:=io.ReadFull(r,b);err!=nil{return Message{},fmt.Errorf("decode frame body: %w",err)};m:=Message{Type:MessageType(b[0]),Fields:map[TLVType][]byte{}};for p:=1;p<int(n);{if p+6>int(n){return Message{},fmt.Errorf("decode TLV header: truncated")};k:=TLVType(binary.BigEndian.Uint16(b[p:p+2]));l:=int(binary.BigEndian.Uint32(b[p+2:p+6]));p+=6;if l<0||p+l>int(n){return Message{},fmt.Errorf("decode TLV: invalid length")};m.Fields[k]=append([]byte(nil),b[p:p+l]...);p+=l};return m,nil}
