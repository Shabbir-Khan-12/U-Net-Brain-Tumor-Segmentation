# user API's
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserModelSerializers, DumpSessionModelSerializers, GetUserSerializer, PredictionImageSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import DumpSession
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import numpy as np
import cv2
from .model_prediction import ModelPrediction
from django.shortcuts import render
from django.http import HttpResponse

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_user_from_jwt(request):
    try:
        user_id = request.user.id
        user = User.objects.get(username=request.user.username)
        # print(request.user.name)
        
        return Response({'user': GetUserSerializer(user).data}, status=200)
    except Exception as e:
        return Response({'error': e}, status=401)


@swagger_auto_schema(methods=['POST'],  request_body=UserModelSerializers)
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def user_gp_controller(request):
    if request.method == 'GET':
        
        users = User.objects.all()
        serializer = UserModelSerializers(users, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        
        serializer = UserModelSerializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(methods=['PUT'],  request_body=UserModelSerializers)
@api_view(['GET', 'PUT', 'DELETE'])
def user_gpd_controller(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserModelSerializers(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserModelSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


# DUMPING SESSION CONTROLLERS
@swagger_auto_schema(methods=['POST'],  request_body=DumpSessionModelSerializers)
@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
def session_gp_controller(request):
    if request.method == 'GET':
        
        dmpsessions = DumpSession.objects.all()
        serializer = DumpSessionModelSerializers(dmpsessions, many=True)
        
        
        
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer = DumpSessionModelSerializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(methods=['PUT'],  request_body=DumpSessionModelSerializers)
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
def session_gpd_controller(request, pk):
    try:
        dmpsession = DumpSession.objects.get(pk=pk)
    except DumpSession.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DumpSessionModelSerializers(dmpsession)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DumpSessionModelSerializers(dmpsession, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        dmpsession.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
def predict_ml_model(request):
    print(request.FILES.get('image'))
    # Initiating Prediction Class Object
    prediction = ModelPrediction(request.FILES.get('image'))

    context = prediction.getPrediction()
    return render(request, 'index.html', context)
    