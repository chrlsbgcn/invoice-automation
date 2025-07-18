# Gunicorn configuration file
bind = "0.0.0.0:10000"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5 minutes for file processing
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True 