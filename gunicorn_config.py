command = '/home/yfpan/CourseDesignPlatform/bin/gunicorn'
pythonpath = '/home/yfpan/CourseDesignPlatform/kaggle'
bind = '127.0.0.1:8001'
workers = 5
debug = True
accesslog = 'log/access.log'
errorlog = 'log/debug.log'

