package main
import("context";"fmt";"os/signal";"syscall";mock "custom-router/test/mock_validator")
func main(){ctx,stop:=signal.NotifyContext(context.Background(),syscall.SIGINT,syscall.SIGTERM);defer stop();s,e:=mock.New(mock.Config{Organization:"NLS-LAB",AuthorizedSerials:map[string]bool{"NLS-TEST-0001":true}});if e!=nil{panic(e)};defer s.Close();fmt.Printf("mock Validator listening on %s\n",s.Addr());<-ctx.Done()}
