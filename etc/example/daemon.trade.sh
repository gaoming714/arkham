source activate
sleep 2

celery -A script.trade worker --loglevel=INFO --pool=eventlet --concurrency=2048 --hostname=trade@TeX --logfile=log/celery.log
