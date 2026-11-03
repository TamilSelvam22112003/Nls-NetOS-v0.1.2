package protocol
import("bufio";"encoding/binary";"encoding/json";"fmt";"io")
// Codec implements a length-prefixed TLV: uint32 frame length, uint16 type, uint32 value length, JSON value.
type Codec struct{r *bufio.Reader}
// NewCodec creates a codec for a stream.
func NewCodec(r io.Reader)*Codec{return &Codec{bufio.NewReader(r)}}
// Write encodes one TLV message.
func Write(w io.Writer,t MessageType,v any)error{b,e:=json.Marshal(v);if e!=nil{return fmt.Errorf("marshal message: %w",e)};p:=make([]byte,6+len(b));binary.BigEndian.PutUint16(p,uint16(t));binary.BigEndian.PutUint32(p[2:],uint32(len(b)));copy(p[6:],b);var h[4]byte;binary.BigEndian.PutUint32(h[:],uint32(len(p)));if _,e=writeAll(w,h[:]);e!=nil{return fmt.Errorf("write frame length: %w",e)};if _,e=writeAll(w,p);e!=nil{return fmt.Errorf("write frame: %w",e)};return nil}
// Read decodes one TLV message.
func(c *Codec)Read(dst any)(MessageType,error){var h[4]byte;if _,e:=io.ReadFull(c.r,h[:]);e!=nil{return 0,fmt.Errorf("read frame length: %w",e)};n:=binary.BigEndian.Uint32(h[:]);if n<6||n>4<<20{return 0,fmt.Errorf("invalid frame length %d",n)};p:=make([]byte,n);if _,e:=io.ReadFull(c.r,p);e!=nil{return 0,fmt.Errorf("read frame: %w",e)};t:=MessageType(binary.BigEndian.Uint16(p));l:=binary.BigEndian.Uint32(p[2:]);if int(l)!=len(p)-6{return 0,fmt.Errorf("invalid TLV length")};if e:=json.Unmarshal(p[6:],dst);e!=nil{return 0,fmt.Errorf("decode message: %w",e)};return t,nil}
func writeAll(w io.Writer,b []byte)(int,error){n:=0;for len(b)>0{m,e:=w.Write(b);n+=m;b=b[m:];if e!=nil{return n,e};if m==0{return n,io.ErrShortWrite}};return n,nil}
