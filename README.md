# ElectricityInfo

## Running

### Server

Make a virtual environment 

```
python3 -m venv env
```

```
source env/bin/activate
```

In CMD

```
 env/Scripts/activate.bat
```

For running the server go to app and install requirements

```
pip install -r requirements.txt
```

Set environment variables 

```
set POSTGRES_USER=<database user>
```

```
POSTGRES_PASSWORD=<password>
```

Run the server 

```
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

To open documentation

```
 http://127.0.0.1:8000/docs
```

For running tests, go to app and run

```
pytest tests/
```

Coverage 

```
coverage run -m pytest tests/
```

Coverage in command line

```
coverage report -m
```

Coverage in a html format

```
coverage html
```

### Client

For running the client you need to install [node](https://nodejs.org/en/download) 

then go to client/react_client

install [typescript](https://www.npmjs.com/package/typescript)

```
npm install -D typescript
```

Vite

```
npm install -D vite
```

Install [recharts](https://www.npmjs.com/package/recharts)

```
npm install recharts
```

Start the client 

```
npm run dev
```



