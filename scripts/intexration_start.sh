# =============================================================== #
# InTeXration startup script
# =============================================================== #

BRed='\e[1;31m'         # Red
BGreen='\e[1;32m'       # Green
NC="\e[m"               # Color Reset

start() {
	nohup python3 -m intexration > /dev/null 2>&1 &
	echo -e "InTeXration ${BGreen}started${NC}."
}

stop() {
	pkill -9 -f intexration
	echo -e "InTeXration ${BRed}stopped${NC}."
}

status() {
	pids=$(pgrep -f intexration)
	if [ $? -eq 1 ]
	then
		echo -e "InTeXration is ${BRed}not running${NC}."
	else
		echo -e "InTeXration is ${BGreen}running${NC}."
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

