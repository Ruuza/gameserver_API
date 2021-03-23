# installation

1. Set the access data for the sql database in `gameServer/config.py`

2. allow/dissable debugging in `run.py`

3. Install requirements with 

```
pip install -r requirements.txt
```

4. init the database with 

```
python create_db_and_insert_values.py
```

5. run the server with 

```
python run.py
```