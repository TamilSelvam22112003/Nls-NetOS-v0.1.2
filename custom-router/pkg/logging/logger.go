package logging
import("io";"log";"os")
// New returns a timestamped router logger.
func New(w io.Writer)*log.Logger{if w==nil{w=os.Stdout};return log.New(w,"custom-router ",log.LstdFlags|log.Lmicroseconds)}
