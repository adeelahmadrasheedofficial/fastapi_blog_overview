#### Creating a virtual environment
* python3 -m venv venv
* source /venv/bin/activate

### Installing FastAPI and start
* Documentation: https://fastapi.tiangolo.com/tutorial
* pip install fastapi[all]
* uvicorn main:app --reload 

### Generating requirement.txt
* pip freeze -r requirements.txt

### Creating DB Schema
#### Why need schema?
* To reterive sanitized data values
* To validate Data
* Getting only data that our app expects
### Using pydantic
* Documentation: https://docs.pydantic.dev/latest/

### Using psycopg for postgres db connetion
* Documentation: https://www.psycopg.org/docs/
* pip install psycopg2