package identity
import "fmt"
// Serial returns a validated router serial number.
func Serial(v string)(string,error){if v==""{return "",fmt.Errorf("serial: empty")};return v,nil}
