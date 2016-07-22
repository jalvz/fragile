import sys, traceback


def zero_division_no_error(app):
    try:
        very_nested_zero_division_no_error(app)
    except ZeroDivisionError:
        pass
    exc_info_1 = sys.exc_info()
    traceback.extract_stack()
    return 'ha!'


def very_nested_zero_division_no_error(app):
    try:
        1 / 0
    except ZeroDivisionError:
        app.logger.error(
            'There was some crazy error',
            exc_info=True)
        exc_info_1 = sys.exc_info()
        raise


def just_log_stuff(app):
    app.logger.warning('Warning!')
    app.logger.error('Error with!')
    app.logger.info('Info - should not be sent')


def deep_zero_division_error():
    return 1 / 0
