# Setup Alembic

To set up Alembic migration management, please follow the instructions below.

1. Create new revision
    ``` bash
    alembic revision -m "create account table"
    ```

    This will set a new directory alembic containing ` versions` 
    which contains all the revised files. 
    Then, a new file 1975ea83b712_create_account_table.py is generated.


2. After creating new file we can include all needed revisions in this file

    ``` bash 
    create account table
    Revision ID: 1975ea83b712
    Revises:
    Create Date: 2011-11-08 11:40:27.089406
    
    # revision identifiers, used by Alembic.
    revision = '1975ea83b712'
    down_revision = None
    branch_labels = None
    
    from alembic import op
    import sqlalchemy as sa
    
    def upgrade():
        pass
    ```
    
* `down_revision` runs an operation, and composes a list based on 
how the `down_revision` identifiers link together with the `down_revision` of `None` representing the first file.

* All information needed to be revised should be included in ` upgrade ` function.

3.  After all revisions completed, run the migration

    ``` bash
     alembic upgrade head
    INFO  [alembic.context] Context class PostgresqlContext.
    INFO  [alembic.context] Will assume transactional DDL.
    INFO  [alembic.context] Running upgrade None -> 1975ea83b712
    ```

All saved changes should be updated or removed by running new revision following steps mentioned above. You can refer to [Alembic official documentation](https://alembic.sqlalchemy.org/en/latest/) for more details.