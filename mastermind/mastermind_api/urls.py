from django.http import HttpResponse
from mastermind_api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

def dummy_http_response(request):
    return HttpResponse('<h2>Hey Mastermind.....</h2>')

def dummy_http_responseV2(request):
    return HttpResponse('<h2>Hey Pradeep.....</h2>')    

urlpatterns = [
    path('wallet_txn/', views.SetBalance.as_view()),
    path('wallet_history/', views.GetAllTransactions.as_view()),
]
