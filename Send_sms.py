import smsru_api
from smsru_api import SmsRu
sms_ru = SmsRu('C51BE417-745B-C0B4-F80D-A71F29127C55')
response = sms_ru.send('9000905976', message='Message to sms')