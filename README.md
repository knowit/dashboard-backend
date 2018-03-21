# dashboard-backend
Backend-server for Sundtkvartalet Dashboard. Proxer og cacher requester mot andre APIer.

## Oppsett
```
# Antar at Python og pip er installert
$ pip install -r requirements.txt
```

## Oppstart
```
$ gunicorn server:app
# eller
$ gunicorn server:app --daemon
```
