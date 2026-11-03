package identity
import "fmt"
// BoardID returns a validated board identifier.
func BoardID(v string)(string,error){if v==""{return "",fmt.Errorf("board id: empty")};return v,nil}
// ChassisNumber returns a validated chassis identifier.
func ChassisNumber(v string)(string,error){if v==""{return "",fmt.Errorf("chassis number: empty")};return v,nil}
