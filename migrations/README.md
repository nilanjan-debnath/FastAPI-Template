# Generic single-database configuration.

## Initialize migrations
```bash
uv run alembic init migrations
```

## Add database url
```python
from app.config import settings

config.set_main_option("sqlalchemy.url", settings.database_url)
```

## Add metadata
```python
from app.db.models import Base

target_metadata = Base.metadata
```

## Autogenerate migrations
```bash
uv run alembic revision --autogenerate -m "message for migrations"
```

## Use the latest version of database
```bash
uv run alembic upgrade head
```


## Useful commands
- Display the current revision for a database `uv run alembic current`
- View migrations history `uv run alembic history --verbose`
- Revert all migrations `uv run alembic downgrade base`
- Revert migrations one by one `uv run alembic downgrade -1`
- Apply all migrations `uv run alembic upgrade head`
- Apply migrations one by one `uv run alembic upgrade +1`
- Display all raw SQL `uv run alembic upgrade head --sql`
- Reset the database `uv run alembic downgrade base && uv run alembic upgrade head`