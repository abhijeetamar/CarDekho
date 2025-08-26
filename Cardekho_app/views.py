from django.shortcuts import render
from .models import Carlist,Showroomlist,Review
# from django.http import JsonResponse,HttpResponse
import json
from .serializers import CarSerializer,ShowroomSerializer,ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework import generics,mixins

class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    authentication_classes=[SessionAuthentication]
    permission_classes = [DjangoModelPermissions]

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)



class ReviewList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)



class Showroom_view(APIView):
    # authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    #permission_classes=[AllowAny]
    #permission_classes=[IsAdminUser]
    authentication_classes=[SessionAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get(self,request):
        showroom = Showroomlist.objects.all()
        serializer = ShowroomSerializer(showroom,many=True,context={'request':request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class Showroom_Details(APIView):
    def get(self,request,pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'Error':'Showroom not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=ShowroomSerializer(showroom)
        return Response(serializer.data)
    
    def put(self,request,pk):
        showroom=Showroomlist.objects.get(pk=pk)
        serializer=ShowroomSerializer(showroom,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status = status.HTTP_204_NO_CONTENT)
    
    def delete(self,request,pk):
        showroom = Showroomlist.objects.get(pk=pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def car_list_view(request):
    if request.method =='GET':
        car=Carlist.objects.all()
        serializer = CarSerializer(car,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer=CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
@api_view(['GET','PUT','DELETE'])
def car_detail_view(request,pk):
    if request.method=='GET':
        try:
            car=Carlist.objects.get(pk=pk)
        except:
            return Response({'Error':'car not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car)
        return Response(serializer.data)
        
    if request.method=='PUT':
        car=Carlist.objects.get(pk=pk)
        serializer=CarSerializer(car,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    if request.method=='DELETE':
        car=Carlist.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
         



    