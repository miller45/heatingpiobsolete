#/!bin/sh
rsync  -av heatingpi:~/python/heatingpi/ . --exclude venv --exclude __pycache__ --exclude .idea --exclude .git --exclude '*.sh' --exclude '*.pyc'
