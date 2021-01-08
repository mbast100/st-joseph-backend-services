# st-joseph-backend-services
#### visit: [stjosephchurch.ca](https://www.stjosephchurch.ca)

## AWS

- setup [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/install-macos.html)
### Lambda deployement
- update prod: `zappa update prod`
- live at: https://zq4r9erb58.execute-api.us-east-1.amazonaws.com/prod

## Developement

### Dev Enviorement
- `python -V` 3.7 or greater.
- clone repo: `git clone https://github.com/mbast100/st-joseph-backend-services.git`
- only cd project root & run (Only required first time):
    - Mac: `python3 -m venv venv`
    - Windows: `python -m venv venv`
- start virtual env:
    - Mac: `source venv\bin\activate`
    - Windows: `source venv\scripts\activate`
- Install requirements: `pip install -r requirements.txt`
- Follow (setup local testing) :
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html

### Start local db
- run `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`

### Create tables
After starting local db.
- run: `cd data/migrations`
- run: `aws dynamodb create-table --cli-input-json file://st_joseph_mails.json --endpoint-url http://localhost:8000`
- run `aws dynamodb create-table --cli-input-json file://st_joseph_media.json --endpoint-url http://localhost:8000`
- run `aws dynamodb create-table --cli-input-json file://srvices.json --endpoint-url http://localhost:8000`
- run `aws dynamodb create-table --cli-input-json file://st_joseph_internal_configurations.json --endpoint-url http://localhost:8000`
- run: `aws dynamodb list-tables --endpoint-url http://localhost:8000`
output should look:
```json
{
    "TableNames": [
        "services",
        "st_joseph_media",
        "st_joseph_mails",
    ]
}
```

### Run App In Testingst

```bash
$ source venv/bin/activate
$ export FLASK_ENV=testing
$ flask run
```
- Run app: `python app.py`

### FLASK

REST API built in [flask](https://flask.palletsprojects.com/en/1.1.x/).

### Testing
https://docs.pytest.org/en/stable/https://docs.pytest.org/en/stable/
#
### Schema validation
Schema validation for input data will be using `schema` pip package.
documentation can be found [here](https://github.com/keleshev/schema).

