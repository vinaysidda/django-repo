from django.urls import path
from eval_app.views import TopProfitableCompaniesView, UploadBusinessExcel,BusinessStatictics,ShivamView,USEmployeeView,HighRevenueCompanies
from eval_app.views import RevenueProfitCorrelationView,StartDataInjection,StopDataInjection,InsetData
 
urlpatterns=[
    path('upload/',UploadBusinessExcel.as_view(),name='upload_business_excel'),
    # path('business/', BusinessList.as_view(), name='list_business'),
    path('business/stats/',BusinessStatictics.as_view(),name='business_stats'),
    # path('business/query/',BusinessQuery.as_view(),name='business_stats'),
    path('shivamapi/',ShivamView.as_view(),name='api_shivam'),
    #path('usdata/',USAEmployeeView.as_view(),name='api_usa'),
    #path('no_of_us_emp/',USEmployeeView.as_view(),name='api_usa_emp'),
   
    path('us-employees/', USEmployeeView.as_view(), name='us-employees'),
    path('profit/', HighRevenueCompanies.as_view(), name='us-employees'),
    path('TopProfi/',TopProfitableCompaniesView.as_view(), name='top-profit-companies'),
    path('Revenucorprofite/',RevenueProfitCorrelationView.as_view(), name='revenue_profit_correlation'),
    path('startDatainjection/',StartDataInjection.as_view(), name='start_datainjection'),
    path('stopDatainjection/', StopDataInjection.as_view(), name='stop_datainjection'),
    path('insertdata/',InsetData.as_view(), name='insert')


    ]
        