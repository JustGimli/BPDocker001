until python3 manage.py makemigrations
do
    echo "Waiting for db to be ready..."
    sleep 3
done

until pip install channels[daphne]
do
    echo "Waiting for db to be ready..."
    sleep 3
done

until python3 manage.py migrate
do
    sleep 3
done


daphne -b 0.0.0.0 -p 8001 config.asgi:application

