package boot

import("context";"fmt";"math/rand";"net";"time")
// RetryPolicy controls exponential backoff, jitter and validator port hopping.
type RetryPolicy struct{Initial,Max time.Duration;Ports []int}
// Retry invokes fn until success or context cancellation, cycling through validator ports.
func(p RetryPolicy)Retry(ctx context.Context,addresses []string,fn func(context.Context,string)error)error{if len(addresses)==0{return fmt.Errorf("retry: no validator addresses")};if len(p.Ports)==0{p.Ports=[]int{12346,12347,12348}};if p.Initial<=0{p.Initial=250*time.Millisecond};if p.Max<=0{p.Max=10*time.Second};d:=p.Initial;for i:=0;;i++{a:=addresses[i%len(addresses)];if h,_,e:=net.SplitHostPort(a);e==nil{a=net.JoinHostPort(h,fmt.Sprint(p.Ports[i%len(p.Ports)]))}else{a=net.JoinHostPort(a,fmt.Sprint(p.Ports[i%len(p.Ports)]))};if e:=fn(ctx,a);e==nil{return nil};if e:=ctx.Err();e!=nil{return fmt.Errorf("retry canceled: %w",e)};j:=time.Duration(rand.Int63n(int64(d/2)+1));wait:=d/2+j;if wait>p.Max{wait=p.Max};t:=time.NewTimer(wait);select{case<-ctx.Done():t.Stop();return fmt.Errorf("retry canceled: %w",ctx.Err());case<-t.C:};if d<p.Max/2{d*=2}else{d=p.Max}}}
