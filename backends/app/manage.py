#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
import dotenv
from django.conf import settings


def main():
    """Run administrative tasks."""
    # settings.configure()
    try:
        from django.core.management import execute_from_command_line
        # external_root = os.path.abspath('/home/user/BP/bot')
        # sys.path.insert(0, external_root)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    dotenv.load_dotenv()

    main()
