package manager
import("context";"fmt";"os";"path/filepath")
// Applier atomically activates downloaded router configuration.
type Applier struct{Path string}
// Apply stages and renames the configuration after honoring context cancellation.
func(a Applier)Apply(ctx context.Context,b []byte)error{select{case<-ctx.Done():return ctx.Err();default:};if a.Path==""{return fmt.Errorf("empty configuration path")};if e:=os.MkdirAll(filepath.Dir(a.Path),0700);e!=nil{return fmt.Errorf("create config directory: %w",e)};tmp:=a.Path+".tmp";if e:=os.WriteFile(tmp,b,0600);e!=nil{return fmt.Errorf("stage configuration: %w",e)};if e:=os.Rename(tmp,a.Path);e!=nil{return fmt.Errorf("activate configuration: %w",e)};return nil}
