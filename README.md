# OSDS-server

# Participants
- [unanchoi](https://github.com/unanchoi)
- [na-yk](https://github.com/na-yk)
- [euije](https://github.com/euije)
- [hi-there-insahae](https://github.com/hi-there-insahae)


## Implementation

##### 0. Virtual Environment
```python
    python -m  venv venv
    source venv/bin/activate
```

##### 1. Run Server

``` pytho
glt clone https://github.com/NodabFamily/OSDS-server.git

python manage.py migrate

python manage.py runserver
```