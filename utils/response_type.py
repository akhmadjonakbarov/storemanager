from utils.response_messages import ResponseMessages


def response_list(lst, pagination={}, message=ResponseMessages.SUCCESS, ) -> dict:
    return {
        'data': {
            'message': message,
            'list': lst,
            'pagination': pagination
        }
    }


def response_item(item, message=ResponseMessages.SUCCESS) -> dict:
    return {
        'data': {
            'message': message,
            'item': item,

        }
    }


def res_error(error) -> dict:
    return {
        'data': {
            'error': error,
        }
    }


def res_message(message) -> dict:
    return {
        'data': {
            'message': message,
        }
    }
