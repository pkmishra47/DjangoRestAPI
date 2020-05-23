from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from mastermind_api.utils.db import DbConnection
from django.views.decorators.csrf import csrf_exempt
from mastermind_api.utils.auth import AccessTokenRequire
from django.core.exceptions import SuspiciousOperation

@method_decorator([csrf_exempt, AccessTokenRequire], name="dispatch")
class SetBalance(APIView):
    '''
    To take care of transaction handling debit/credit of amount from a specific account.
    It looks for three values (contact_number, amount,trantype) to make a transaction.
    '''
    def __init__(self):
        pass

    def post(self, request, **kwargs):
        response = {}
        try:
            if kwargs["is_validate"] is True:
                parameters = []
                request_details = request.data

                if 'contact_number' in request_details:
                    parameters.append(str(request_details['contact_number']))
                else:
                    return Response("contact_number doesn't exist in request.")

                if 'amount' in request_details:
                    parameters.append(float(request_details['amount']))
                else:
                    return Response("amount doesn't exist in request.")

                if 'trantype' in request_details:
                    parameters.append(request_details['trantype'])
                else:
                    return Response("trantype doesn't exist in request.")      

                parameters.append('')
                db_conn = DbConnection()
                response = db_conn.execute_statement(proc_name= "sp_set_balance", commit= True, params = parameters)
                message,status = "",False

                if response.get_ErrorMessage():
                    message = response.get_ErrorMessage()
                else:
                    message = response.get_Params()[len(parameters)-1]
                    status = True

                return Response({"Message":message,"Data":None,"Status":status})
            else:
                raise SuspiciousOperation("Access Token Require!!!!")
        except Exception as error:
            raise SuspiciousOperation("Bad Request " + str(error))
        
@method_decorator([csrf_exempt,AccessTokenRequire],name="dispatch")
class GetAllTransactions(APIView):
    '''
    To list all transaction on most recent first fashion. Request should have contact_number,offset
    and total_count parameters in request. 
    
    '''
    def __init__(self):
        pass

    def post(self, request, **kwargs):    
        response = {}
        try:
            if kwargs["is_validate"] is True:   
                parameters = []
                request_details = request.data

                if 'contact_number' in request_details:
                    parameters.append(request_details['contact_number'])
                else:
                    return Response("contact_number doesn't exist in request.")

                if 'offset' in request_details:
                    parameters.append(request_details['offset'])
                else:
                    return Response("offset doesn't exist in request.")

                if 'total_count' in request_details:
                    parameters.append(request_details['total_count'])
                else:
                    return Response("total_count doesn't exist in request.")

                parameters.append('')
                db_conn = DbConnection()
                response = db_conn.execute_statement(proc_name= "sp_get_transaction_details", commit= True, params = parameters)
                message, status, data  = "", False, None

                if response.get_Data():
                    data = response.get_Data()[0]
                    status = True
                elif response.get_ErrorMessage():
                    message = response.get_ErrorMessage()
                else:
                    message = response.get_Params()[len(parameters)-1]

                return Response({"Message":message,"Data":data,"Status":status})
            else:
                raise SuspiciousOperation("Access Token Require!!!!")
        except Exception as error:
            raise SuspiciousOperation("Bad Request " + str(error))        