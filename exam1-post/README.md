# fastapi-tutorial
fastapi tutorial
* install
```bash
$ pip install fastapi uvicorn

```

* run server
```bash
$ uvicorn main:app --reload
$ uvicorn main:app --host 0.0.0.0 --port 8000 --reload
$ uvicorn main:app -host 0.0.0.0 -port 8001 -reload -workers 4
```

### JWT

```bash
$ pip install fastapi[all] python-jose[cryptography] passlib[bcrypt]
$ pip install sqlalchemy
$ pip install sqlite
$ pip install python-jose[cryptography]
$ pip install -U pytest
```

### kill process
```bash
## for windows
> tasklist | findstr uvicorn
uvicorn.exe                  20880 Console                    1      7,676 K

> taskkill /PID 20880 /F
```