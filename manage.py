import os
import sys
from pathlib import Path

def main():
    """Run administrative tasks."""
    # Recommendation: Use os.getenv to toggle settings dynamically
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'core.settings.dev'))
    
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(os.path.join(BASE_DIR, 'apps'))
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed?") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
