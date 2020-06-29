import eel
import json
import datetime

eel.init('web')

@eel.expose
def py_json_data_sender():
    return {
        'datetime': datetime.datetime.now()
    }

@eel.expose
def py_json_data_loader():
    return eel.js_json_data_sender()(print_value)

def print_value(v):
    print('Got this value from javascript:')
    print(v)

# Custom Json Encoder.
class EelJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.__str__()


# Custom Json Decoder.
class CustomDatetimeObj(object):
    def __init__(self, datetime):
        self.datetime = datetime

    def __str__(self):
        return 'CustomDatetimeObj: %s' % self.datetime.__str__()

def decoder_object_hook(o):
    if 'datetime' in o:
        return CustomDatetimeObj(datetime=o['datetime'])
    else:
        return o

class EelJsonDecoder(json.JSONDecoder):
    def __init__(self, object_hook=decoder_object_hook, *args, **kwargs):
        super().__init__(object_hook=object_hook, *args, **kwargs)


eel.start('custom_json_encoder_decoder.html', json_encoder=EelJsonEncoder,
          json_decoder=EelJsonDecoder, size=(400, 300))
