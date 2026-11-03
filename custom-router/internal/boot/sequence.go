package boot
import("context";"fmt";"io";"log";"net";"custom-router/config";"custom-router/internal/protocol")
// State identifies a router onboarding state.
type State string
const(StateInit State="Init";StateEnroll State="Enroll";StateValidatorHandshake State="ValidatorHandshake";StateDiscoverControllers State="DiscoverControllers";StateControllerConnect State="ControllerConnect";StateFetchConfig State="FetchConfig";StateRunning State="Running";StateBackoff State="Backoff")
// Hooks provides the operations executed by the state machine.
type Hooks struct{Enroll func(context.Context)error;Handshake func(context.Context,string)(io.ReadWriteCloser,error);Discover func(context.Context,io.ReadWriter)([]protocol.ControllerEndpoint,error);ControllerConnect func(context.Context,[]protocol.ControllerEndpoint)error;FetchConfig func(context.Context,[]protocol.ControllerEndpoint)([]byte,error);ApplyConfig func(context.Context,[]byte)error}
// Sequence is the explicit onboarding state machine.
type Sequence struct{Log *log.Logger;Config config.Config;Retry RetryPolicy;Hooks Hooks;State State}
func(s *Sequence)transition(n State){if s.Log!=nil{s.Log.Printf("state transition: %s -> %s",s.State,n)};s.State=n}
// Run executes the state machine and retries all errors through Backoff.
func(s *Sequence)Run(ctx context.Context)error{for{e:=s.runOnce(ctx);if e==nil{return nil};if ctx.Err()!=nil{return ctx.Err()};s.transition(StateBackoff);port,x:=s.Retry.Next(ctx);if x!=nil{return x};s.Config.Validator=replacePort(s.Config.Validator,port)}}
func(s *Sequence)runOnce(ctx context.Context)error{if s.State==""{s.State=StateInit;s.transition(StateInit)}else{s.transition(StateInit)};if s.Config.AutoEnroll&&s.Hooks.Enroll!=nil{s.transition(StateEnroll);if e:=s.Hooks.Enroll(ctx);e!=nil{return fmt.Errorf("enrollment: %w",e)}};s.transition(StateValidatorHandshake);conn,e:=s.Hooks.Handshake(ctx,s.Config.Validator);if e!=nil{return fmt.Errorf("validator handshake: %w",e)};s.transition(StateDiscoverControllers);eps,e:=s.Hooks.Discover(ctx,conn);closeErr:=conn.Close();if e!=nil{return fmt.Errorf("discover controllers: %w",e)};if closeErr!=nil{return fmt.Errorf("close Validator connection: %w",closeErr)};s.transition(StateControllerConnect);if e=s.Hooks.ControllerConnect(ctx,eps);e!=nil{return fmt.Errorf("controller connect: %w",e)};s.transition(StateFetchConfig);b,e:=s.Hooks.FetchConfig(ctx,eps);if e!=nil{return fmt.Errorf("fetch config: %w",e)};if s.Hooks.ApplyConfig!=nil{if e=s.Hooks.ApplyConfig(ctx,b);e!=nil{return fmt.Errorf("apply config: %w",e)}};s.transition(StateRunning);s.Retry.Reset();return nil}
func replacePort(a string,p int)string{h,_,e:=net.SplitHostPort(a);if e!=nil{return net.JoinHostPort(a,fmt.Sprint(p))};return net.JoinHostPort(h,fmt.Sprint(p))}
