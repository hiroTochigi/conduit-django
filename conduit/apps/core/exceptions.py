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
        'NotFound': _handle_not_found_error,
        "ValidationError": _handle_generic_error,
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

def _handle_not_found_error(exc, context, response):
    view = context.get('view', None)

    # the view must have specified a queryset property
    # ArticleViewSet should have queryset
    # Because we set up the queryset
    if view and getattr(view, 'queryset') is not None and view.queryset is not None:
        error_key = view.queryset.model._meta.verbose_name

        response.data = {
            'errors': {
                error_key: response.data['detail']
            }
        }

    else:
        response = _handle_generic_error(exc, context, response)

    return response