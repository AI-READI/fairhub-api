### Setup Alembic


Alembic leverages SQLAlchemy as its underlying engine to facilitate the creation, 
management, and execution of change management scripts for relational databases. 
To set up Alembic for migration management, please follow the instructions below.


1.Install alembic
   ```
 pip install Flask-Alembic
   ```

2.Create new revision
```
alembic revision -m "create account table"
```

3.Make a revision in the ```create account table``` file

``` 
def upgrade():
    pass
```

4.After all revisions completed, run the migration

```
alembic upgrade head
```

5.Running our Second Migration
```
alembic revision -m "Add a column"
```
