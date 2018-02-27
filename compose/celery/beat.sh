#!/bin/sh

/usr/local/bin/celery -A sample.taskapp beat -l info
