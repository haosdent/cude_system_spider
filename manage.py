#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cude_system_spider.settings")

    from django.core.management import execute_from_command_line
    from gevent import monkey
    monkey.patch_all()

    execute_from_command_line(sys.argv)
