# Exit if any command fails
set -o errexit

pip install -r requirements.txt

# Run migrations automatically
python manage.py migrate

# Seed your products (Mantra Wireless, etc.)
python seed_data.py

# Collect CSS/Images
python manage.py collectstatic --no-input
