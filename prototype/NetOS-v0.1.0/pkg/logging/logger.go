package logging
import "log/slog"
// Logger is the boot logging interface.
type Logger interface{Info(string,...any);Warn(string,...any);Error(string,...any)}
// New returns the process default structured logger.
func New()Logger{return slog.Default()}
