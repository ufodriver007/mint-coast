FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 

WORKDIR /code 

RUN pip install --upgrade pip 
RUN apt update && apt -y install curl

COPY . /code/

RUN pip install -r requirements.txt

RUN chmod 777 recapcha_replace
RUN ./recapcha_replace

CMD python manage.py makemigrations \
        && python manage.py migrate \
        && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" \
        && python manage.py loaddata /code/fixtures/mint_app/category.json \
        && python manage.py loaddata /code/fixtures/socialaccount/socialapp.json \
        && python manage.py loaddata /code/fixtures/sites/site.json \
        && python manage.py collectstatic --no-input \
        && gunicorn mint_coast.wsgi:application --bind 0.0.0.0:8000 --log-level info
