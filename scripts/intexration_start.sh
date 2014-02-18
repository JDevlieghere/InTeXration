# =============================================================== #
# InTeXration startup script
# =============================================================== #

start() {
	nohup python3 -m intexration > /dev/null 2>&1 &
	echo -e "InTeXration started."
}

stop() {
	pkill -9 -f intexration
	echo -e "InTeXration stopped$."
}

status() {
	pids=$(pgrep -f intexration)
	if [ $? -eq 1 ]
	then
		echo "InTeXration is not running."
	else
		echo "InTeXration is running."
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
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac
exit 0

