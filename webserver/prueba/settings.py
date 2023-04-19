DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dogsorcats',
        'USER': 'tfgadmin',
        'PASSWORD': 'tfgdatabase',
        'HOST': '10.0.20.20',
        'PORT': '5432',
    }
}

# Enviar logs a ELK
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': CustomJsonFormatter,
            'format': '%(asctime)s %(levelname)s %(message)s',
        }
    },
    'handlers': {
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': '10.0.20.10',  
            'port': 5000,  
            'version': 1,
            'message_type': 'logstash',
            'fqdn': True,
            'tags': ['django'],
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}