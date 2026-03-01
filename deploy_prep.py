import os
import subprocess
import sys

def run_command(command):
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Error executing: {command}")
        sys.exit(1)

def prepare_deployment():
    # 1. Clear old static files
    print("Clearing old static files...")
    run_command("python manage.py collectstatic --noinput --clear")

    # 2. Check for missing migrations
    print("Checking for model changes...")
    run_command("python manage.py makemigrations")

    # 3. Apply migrations
    print("Syncing database...")
    run_command("python manage.py migrate")

    print("\n✅ Mantra24 Deployment Preparation Complete!")

if __name__ == "__main__":
    prepare_deployment()
