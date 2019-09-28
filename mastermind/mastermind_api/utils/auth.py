import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "conf.ini"))

TOKEN = config['Oauth']['token']

class AccessTokenRequire(object):
    '''
    Authenticates each request by validating static token provided to logged in user at the time 
    of login. This is for dev purpose and can be replaced by userwise token validation for 
    production (Not part of this project at this moment.)
    '''
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        token_validation_res = {"is_validate": False}
        request = args[0]
        
        if 'HTTP_AUTHORIZATION' in request.META:
            token = request.META['HTTP_AUTHORIZATION']
            if self.__is_valid_access_token(token):
                token_validation_res["is_validate"] = True
        kwargs.update(token_validation_res)

        return self.func(*args, **kwargs)

    def __is_valid_access_token(self, passed_token):
        try:
            if passed_token.split(' ')[1] == TOKEN:
                return True
        except:
            return False