
import collections

from ... import FailPage, GoTo, ValidateError, ServerError
from .. import hardware


def sensor_table01(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    """sets two lists for sensor table 01 into page data"""
    sensors = hardware.get_input_names()
    page_data['table01', 'col1'] = sensors
    page_data['table01', 'col2'] = _get_sensor_values(sensors)


def sensors_json_api(caller_ident, ident_list, submit_list, submit_dict, call_data, page_data, lang):
    "Returns sensors dictionary"
    sensors = hardware.get_input_names()
    values = _get_sensor_values(sensors)
    return collections.OrderedDict(zip(sensors,values))


def _get_sensor_values(sensors):
    "Returns list of sensor values"
    values = []
    for name in sensors:
        input_type = hardware.get_input_type(name)
        if input_type == 'boolean':
            invalue = hardware.get_boolean_input(name)
            if invalue is None:
                value = 'UNKNOWN'
            elif invalue:
                value = 'ON'
            else:
                value = 'OFF'
        elif input_type == 'text':
            value = hardware.get_text_input(name)
        else:
            value = ''
        values.append(value)
    return values
