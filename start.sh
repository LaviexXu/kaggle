#!/bin/bash
../bin/gunicorn -c gunicorn_config.py kaggle.wsgi
