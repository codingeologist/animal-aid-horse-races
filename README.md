# Animal Aid Race Horse Watch

## setup venv
```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## build docker image
```bash
export APP_VERSION=0.1
docker build --tag animal-aid-horse-races:$APP_VERSION .
```

### show docker images
```bash
docker images
```

### run docker image
```bash
docker run -d -p 8501:8501 animal-aid-horse-races:$APP_VERSION
```

[http://localhost:8501](http://localhost:8501)