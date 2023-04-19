from pythonjsonlogger import jsonlogger
from datetime import datetime

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        log_record = self._update_record_with_custom_data(record)
        return (super().format(log_record) + '\n').encode('utf-8')

    def _update_record_with_custom_data(self, record):
        record.timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return record
