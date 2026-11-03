package netutil
import "context"
// NATInfo describes conservative NAT detection state.
type NATInfo struct{Detected bool;PublicAddress string}
// DetectNAT intentionally does not infer NAT from local-only information.
func DetectNAT(ctx context.Context)(NATInfo,error){if e:=ctx.Err();e!=nil{return NATInfo{},e};return NATInfo{},nil}
