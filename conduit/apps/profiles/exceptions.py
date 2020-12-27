from rest_framework.exceptions import APIException 

# Make Customized DoesBotExist -> APIException is overridden 
# then modify status_code and default_detail   
class ProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested profile does not exist.'


#This is a simple exception. In Django REST Framework, any time you want to create a custom exception, you inherit from APIException. All you have to do then is specify the default_detail and status_code properties. The default of this exception can be overridden on a case-by-case basis if you decide that makes the most sense.