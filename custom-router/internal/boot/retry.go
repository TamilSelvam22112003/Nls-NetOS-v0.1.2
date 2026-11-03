package boot
import("context";"fmt";"math/rand";"time")
// RetryPolicy implements exponential backoff with jitter and port hopping.
type RetryPolicy struct{Initial,Max time.Duration;Ports []int;attempt int;rnd *rand.Rand}
// Next waits and returns the next Validator port.
func(r *RetryPolicy)Next(ctx context.Context)(int,error){if len(r.Ports)==0{return 0,fmt.Errorf("no validator ports")};if r.Initial<=0{r.Initial=250*time.Millisecond};if r.Max<r.Initial{r.Max=r.Initial};if r.rnd==nil{r.rnd=rand.New(rand.NewSource(time.Now().UnixNano()))};base:=r.Initial;for i:=0;i<r.attempt;i++{if base>=r.Max{base=r.Max;break};base*=2;if base>r.Max{base=r.Max}};j:=time.Duration(r.rnd.Int63n(int64(base/4)+1));wait:=base/2+j;if wait>r.Max{wait=r.Max};t:=time.NewTimer(wait);defer t.Stop();select{case<-ctx.Done():return 0,ctx.Err();case<-t.C:r.attempt++};return r.Ports[(r.attempt-1)%len(r.Ports)],nil}
// Reset clears retry history.
func(r *RetryPolicy)Reset(){r.attempt=0}
// Attempt returns completed retry waits.
func(r *RetryPolicy)Attempt()int{return r.attempt}
