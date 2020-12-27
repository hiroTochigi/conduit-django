from rest_framework.views import exception_handler 

# When exception is raised by Django, this function is called because 
# The function is explicitly configured on settings.py like below

# REST_FRAMEWORK = {
#    'EXCEPTION_HANDLER': 'conduit.apps.core.exceptions.core_exceptionhandler',
#     ...
#   }

def core_exceptionhandler(exc, context):

    response = exception_handler(exc, context)
    handlers = {
        "ValidationError": _handle_generic_error,
        "ProfileDoesNotExist": _handle_generic_error,
    }

    # Get exception class name
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response

def _handle_generic_error(exc, context, response):

    response.data = {
        "error": response.data
    }
    return response