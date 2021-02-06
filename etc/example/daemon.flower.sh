source activate
# flower, which is used for check celery, is in alpha

echo celery flower -A script.trade --address=127.0.0.1 --port=5555 --broker=redis://127.0.0.1:6379//

