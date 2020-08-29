# Wikiracer

![alt text](https://github.com/kompotkot/WebScraper-Wikiracer/blob/master/output.png?raw=true)

## Install module
```
pip install -e .
```

## Run wikiracer
```
wikiracer-app -o wikipedia.org -s /wiki/Battle_of_Cr%C3%A9cy -f /wiki/Sweden
```

## Alembic generate DB
```
> cd wikiracer
> alembic init db/alembic
```

## Set config in alembic.ini and env.py
```
wikiracer-db revision --message="Initial" --autogenerate
wikiracer-db upgrade head
```

## Add test data to DB
```
INSERT INTO urls (link, parent, depth, parsed) VALUES ('/wiki/Battle_of_Cr%C3%A9cy', '/wiki/Sweden', 0, False);
```
