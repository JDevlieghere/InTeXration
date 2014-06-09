# =============================================================== #
# InTeXration startup script
# =============================================================== #

start() {
	nohup python3 -m intexration > /dev/null 2>&1 &
	echo "InTeXration started."
}

stop() {
	pkill -9 -f 'python3.*intexration'
	echo "InTeXration stopped."
}

status() {
	pids=$(pgrep -f 'python3.*intexration')
	if [ "${pids}" ]; then
		echo "InTeXration is running."
	else
		echo "InTeXration is not running."
	fi
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        status
        ;;
  restart|reload|condrestart)
        stop
        start
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac
exit 0

