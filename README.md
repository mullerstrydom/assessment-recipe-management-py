# assessment-recipe-management-py

## Background
This project is created in python. And uses sqlmodel and fastapi dependencies. 

## Architecture
- FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints.
- SqlModel is a library for interacting with SQL databases from Python code using type annotations. It is built on top of 
SQLAlchemy and Pydantic, providing a simple and intuitive way to define database models and perform database operations.
- Sqlite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database 
engine.

## Start the application
Before starting the application:
- make sure you have installed the dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```
- make sure you have set PYTHONPATH to the root project folder. For example, from the root project folder:
```bash
export PYTHONPATH=$(pwd)/recipe_management:$PYTHONPATH
```

The following command can be used from the root project folder to start the application:
```bash
python recipe_management/main.py --log-file-name=TEST
```

The log file `TEST.log` will be created in the root project folder.

### Other start parameters
```text
usage: main.py [-h] --log-file-name LOG_FILE_NAME
               [--log-level {DEBUG,INFO,WARN,ERROR}]
               [--log-file-size LOG_FILE_SIZE]
               [--log-backup-count LOG_BACKUP_COUNT]
               [--http-address HTTP_ADDRESS] [--http-port HTTP_PORT]
               [--db-url DB_URL]

Recipe management

options:
  -h, --help            show this help message and exit
  --log-file-name LOG_FILE_NAME
                        Log file name
  --log-level {DEBUG,INFO,WARN,ERROR}
                        Log level name
  --log-file-size LOG_FILE_SIZE
                        File size of each log file in MB
  --log-backup-count LOG_BACKUP_COUNT
                        Number of backup log files to keep
  --http-address HTTP_ADDRESS
                        The address of the HTTP server
  --http-port HTTP_PORT
                        The port of the HTTP server
  --db-url DB_URL       The address of the database server
```

### To persist the database to a file.db
To persist the database to a file, you can start the application with the following command:
```bash
python recipe_management/main.py --db-url=sqlite://recipe_management.db --log-file-name=TEST
```

The sqlite database file `recipe_management.db` will be created in the root project folder.

## Manually Testing the webservices

The following http files have preset http requests that can be executed from jetbrains IDE:
- `test/http/recipes-get.http`  To get a recipe
- `test/http/recipes-post.http` To create a recipe
- `test/http/recipes-put.http` To update a recipe
- `test/http/recipes-delete.http` To delete a recipe

The `http-client.env.json` will help with the server (localhost) you are connected to, and the user to use.


## Rest API Documentation
- Openapi [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- Swagger [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc [http://localhost:8000/redoc](http://localhost:8000/redoc)