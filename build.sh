set -o errexit

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running database migrations..."
python manage.py migrate

echo "Initializing groups and permissions..."
python manage.py initialize_groups
