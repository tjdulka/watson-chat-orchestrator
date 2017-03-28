git pull
kill `cat gunicorn.pid `
nohup sh run.sh &
tail -n 10 nohup.out
