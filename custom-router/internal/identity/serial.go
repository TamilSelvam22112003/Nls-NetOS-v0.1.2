package identity
import "fmt"
// Identity contains stable router identity values.
type Identity struct{Serial,Chassis,BoardID string}
// Validate checks that all stable identity fields are present.
func(i Identity)Validate()error{if i.Serial==""||i.Chassis==""||i.BoardID==""{return fmt.Errorf("serial, chassis and board ID are required")};return nil}
