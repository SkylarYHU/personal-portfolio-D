web: gunicorn portfolio.wsgi --log-file -
release: python3 manage.py migrate && python3 manage.py init_data