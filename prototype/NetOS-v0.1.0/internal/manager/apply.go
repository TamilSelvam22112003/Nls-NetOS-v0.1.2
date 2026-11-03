package manager
import("fmt";"os")
// Apply persists fetched configuration with restrictive permissions.
func Apply(path string,data []byte)error{if path==""{return fmt.Errorf("apply config: empty path")};if e:=os.WriteFile(path,data,0600);e!=nil{return fmt.Errorf("apply config: %w",e)};return nil}
