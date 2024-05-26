LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
      'simple': {
            'format': 'velname)s %(message)s'
        },
  },
  'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'logstash',
            'port': 5000, 
            'version': 1,
            'message_type': 'django',  # 'type' поле для logstash сообщения.
            'fqdn': False,
            'tags': ['django'], # список тег.
        },
  },
  'loggers': {
        'django.request': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}