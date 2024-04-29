from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class PassOldTestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PassOrtTestSerializer

    def post(self, request, pk):
        serializer_context = {'request': request, 'pk': pk}
        serializer = PassOrtTestSerializer(data=request.data, context=serializer_context, many=True)
        
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response("Test completed successfully", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class StartTestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StartTestSerializer

    def post(self, request):
        serializer_context = {'request': request}
        serializer = StartTestSerializer(data=request.data, context=serializer_context)
        
        if serializer.is_valid():
            serializer.create_results(serializer.validated_data)
            return Response("Test started", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PassTestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PassTestSerializer

    def post(self, request):
        serializer_context = {'request': request}
        serializer = PassTestSerializer(data=request.data, context=serializer_context)
        
        if serializer.is_valid():
            serializer.check_answer(serializer.validated_data)
            return Response("Ответ принят", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class FinishTestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FinishTestSerializer

    def post(self, request):
        serializer_context = {'request': request}
        serializer = FinishTestSerializer(data=request.data, context=serializer_context)
        
        if serializer.is_valid():
            serializer.finalize_response(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)