import json
import os

from cerberus import errors
from cerberus.errors import BasicErrorHandler


class CustomError(BasicErrorHandler):
    messages = BasicErrorHandler.messages.copy()
    file = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'status_codes.json')
    with open(file) as f:
        my_status = json.load(f)
    messages[errors.BAD_TYPE.code] = my_status['BAD_TYPE']
    messages[errors.MAX_LENGTH.code] = my_status['MAX_LENGTH']
    messages[errors.DEPENDENCIES_FIELD.code] = my_status['DEPENDENCIES_FIELD']
    messages[errors.REQUIRED_FIELD.code] = my_status['REQUIRED_FIELD']
    messages[errors.DEPENDENCIES_FIELD_VALUE.code] = my_status['DEPENDENCIES_FIELD_VALUE']
    messages[errors.EXCLUDES_FIELD.code] = my_status['EXCLUDES_FIELD']
    messages[errors.EMPTY_NOT_ALLOWED.code] = my_status['EMPTY_NOT_ALLOWED']
    messages[errors.NOT_NULLABLE.code] = my_status['NOT_NULLABLE']
    messages[errors.BAD_TYPE_FOR_SCHEMA.code] = my_status['BAD_TYPE_FOR_SCHEMA']
    messages[errors.ITEMS_LENGTH.code] = my_status['ITEMS_LENGTH']
    messages[errors.MIN_LENGTH.code] = my_status['MIN_LENGTH']
    messages[errors.REGEX_MISMATCH.code] = my_status['REGEX_MISMATCH']
    messages[errors.MIN_VALUE.code] = my_status['MIN_VALUE']
    messages[errors.MAX_VALUE.code] = my_status['MAX_VALUE']
    messages[errors.UNALLOWED_VALUE.code] = my_status['UNALLOWED_VALUE']
    messages[errors.UNALLOWED_VALUES.code] = my_status['UNALLOWED_VALUES']
    messages[errors.FORBIDDEN_VALUE.code] = my_status['FORBIDDEN_VALUE']
    messages[errors.FORBIDDEN_VALUES.code] = my_status['FORBIDDEN_VALUES']
    messages[errors.COERCION_FAILED.code] = my_status['COERCION_FAILED']
    messages[errors.RENAMING_FAILED.code] = my_status['RENAMING_FAILED']
    messages[errors.READONLY_FIELD.code] = my_status['READONLY_FIELD']
    messages[errors.SETTING_DEFAULT_FAILED.code] = my_status['SETTING_DEFAULT_FAILED']
    messages[errors.MAPPING_SCHEMA.code] = my_status['MAPPING_SCHEMA']
    messages[errors.SEQUENCE_SCHEMA.code] = my_status['SEQUENCE_SCHEMA']
    messages[errors.KEYSCHEMA.code] = my_status['KEYSCHEMA']
    messages[errors.VALUESCHEMA.code] = my_status['VALUESCHEMA']
    messages[errors.BAD_ITEMS.code] = my_status['BAD_ITEMS']

    def _format_message(self, field, error):
        try:
            self.messages[error.code]['message_en'] = self.messages[error.code]['message_en'].format(
                *error.info, constraint=error.constraint, field=field, value=error.value
            )
            self.messages[error.code]['message_fa'] = self.messages[error.code]['message_fa'].format(
                *error.info, constraint=error.constraint, field=field, value=error.value
            )
            self.messages[error.code]['field'] = self.messages[error.code]['field'].format(
                *error.info, constraint=error.constraint, field=field, value=error.value
            )
            self.messages[error.code]['explanation'] = self.messages[error.code]['explanation'].format(
                *error.info, constraint=error.constraint, field=field, value=error.value
            )
        except:
            self.messages[error.code] = self.messages[error.code].format(
                *error.info, constraint=error.constraint, field=field, value=error.value
            )
        return self.messages[error.code]
