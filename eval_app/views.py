from django.shortcuts import render

from.serializers import GPTSerializer
from.models import GPT

from django.shortcuts import render
from django.contrib import admin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Business
from .serializers import BusinessSerializer
import pandas as pd
import numpy as np
from django.db.models import Count, Avg, Sum
from .Genearate import inject_data
from threading import Thread, Event

data_injection_thread = None
stop_event = Event()


from rest_framework import viewsets
class GPTViewSet(viewsets.ModelViewSet):
    queryset = GPT.objects.all()
    serializer_class = GPTSerializer



class UploadBusinessExcel(APIView):
    count=0
    def post(self,request):
        excel_file=request.FILES['office']
        df=pd.read_excel(excel_file)
        
        for _, row in df.iterrows():
            Business.objects.create(
                name=row['name'],
                revenue=row['revenue'],
                profit=row['profit'],
                employees=row['employees'],
                country=row['country'],
 
            )
            self.count = self.count+1
        print(self.count)
 
        return Response({"message":"Business data Uploaded now"},status=status.HTTP_201_CREATED)
 
 
 
 
class BusinessStatictics(APIView):
    def get(self,request):
        business_data=Business.objects.values_list('revenue','profit','employees')
        d_data=Business.objects.filter(country='USA')
        np_data=np.array(business_data)
        stats={
            'mean':np.mean(np_data,axis=1).tolist(),
            'std_dev':np.std(np_data,axis=1).tolist(),
            'min':np.min(np_data,axis=1).tolist(),
            # 'data':list(d_data)
        }
        return Response(stats)
    
 
 
 
class ShivamView(APIView):
    def get(self,request):
 
        return Response({"message":"Shivam's Message"})
 
 
 
# find all the employees in USA
class USEmployeeView(APIView):
    def get(self,request):
        #excel_file=request.FILES['office']
        emp_data = Business.objects.filter(country='USA')
        emp_data1=pd.DataFrame(emp_data)
        emp_data2=emp_data1['employees'].sum()
        #df=pd.read_excel(excel_file)
        #emp_data=df[df['country']=='USA']['employees'].sum()
        return Response({"Number of Us Employee":emp_data2})

class HighRevenueCompanies(APIView):
    def get(self, request):
        companies = Business.objects.filter(revenue__gt=50000).values_list('name', flat=True)
        return Response({"Companies with Revenue > 50000": list(companies)})
 
class TopProfitableCompaniesView(APIView):
    def get(self, request):
        top_profitable_companies = Business.objects.order_by('-profit')[:5]
        companies_data = list(top_profitable_companies.values('name', 'profit'))
        return Response({"Top 5 Most Profitable Companies": companies_data})

class RevenueProfitCorrelationView(APIView):
    def get(self, request):
        # Fetch data using Django ORM
        revenue_profit_data = Business.objects.values('revenue', 'profit')
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(list(revenue_profit_data))
        
        # Calculate correlation
        correlation = df['revenue'].corr(df['profit'])
        
        return Response({"Correlation between Revenue and Profit": correlation})


class StartDataInjection(APIView):
    def post(self, request):
        global data_injection_thread
        global stop_event
        
        if data_injection_thread is None or not data_injection_thread.is_alive():
            stop_event.clear()
            data_injection_thread = Thread(target=inject_data, args=(stop_event,))
            data_injection_thread.start()
            
            return Response({"message": "Data injection started"})
        else:
            return Response({"message": "Data injection is already in progress"}, status=status.HTTP_409_CONFLICT)
        
class StopDataInjection(APIView):
    def post(self, request):
        global data_injection_thread
        stop_event.set()
        if data_injection_thread and data_injection_thread.is_alive():
            data_injection_thread.join()
            data_injection_thread = None
        return Response({"message": "Data injection stopped."}, status=status.HTTP_200_OK)
    
class InsetData(APIView):
    def post(self, request):
        # Initialize the serializer with the request data
        serializer = BusinessSerializer(data=request.data)
        
        # Validate the data
        if serializer.is_valid():
            # Save the validated data to the database
            serializer.save()
            return Response({"message": "Data inserted successfully."}, status=status.HTTP_201_CREATED)
        else:
            # Return validation errors if the data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

