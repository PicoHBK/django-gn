#!/bin/sh
set -e

echo "Esperando a Postgres..."
until python - <<'PY'
import os, socket, sys, urllib.parse as up
u = up.urlparse(os.environ["DATABASE_URL"])
s = socket.socket()
s.settimeout(2)
try:
    s.connect((u.hostname, u.port or 5432))
except OSError:
    sys.exit(1)
PY
do
    sleep 1
done
echo "Postgres listo."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Carga el backup solo la primera vez (si la base esta vacia)
if [ "${LOAD_FIXTURE}" = "1" ]; then
    if python manage.py shell -c "
from generate.models import Character
import sys
sys.exit(0 if Character.objects.exists() else 1)
" 2>/dev/null; then
        echo "La base ya tiene datos, no se carga el fixture."
    else
        echo "Base vacia -> cargando backup_postgres_clean.json"
        python manage.py loaddata backup_postgres_clean.json
    fi
fi

exec gunicorn server.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
