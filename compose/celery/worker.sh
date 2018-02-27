#!/bin/sh

/usr/local/bin/celery -A sample.taskapp worker -Q celery -l info -n sample@%h
