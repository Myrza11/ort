from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status, generics
from drf_spectacular.utils import extend_schema

# Create your views here.


class PassTestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PassOrtTestSerializer
    
    @extend_schema(tags=['OrtPass'])
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

    @extend_schema(tags=['OrtPass'])
    def post(self, request):
        serializer_context = {'request': request}
        serializer = StartTestSerializer(data=request.data, context=serializer_context)
        
        if serializer.is_valid():
            questions = serializer.create_results(serializer.validated_data)
            question_data = GetQuestionSerializer(questions, many=True).data  # Serialize the questions
            return Response(question_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = GetSubjectSerializer
    queryset = Subject.objects.all()

    @extend_schema(tags=['OrtList'])
    def get_subject(self):
         return self.queryset

class TestListView(generics.ListAPIView):
    serializer_class = GetTestSerializer

    @extend_schema(tags=['OrtList'])
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Test.objects.filter(subject_id=pk)
    

class QuestionListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = GetQuestionSerializer
    queryset = Question.objects.all()

    @extend_schema(tags=['OrtList'])    
    def get_question(self):
        pk = self.kwargs['pk']
        queryset = Question.objects.filter(topic_id=Topics.objects.get(id=pk))
        if len(queryset) is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return queryset


class ResultsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTestSerializer
    queryset = Results.objects.all()

    @extend_schema(tags=['OrtList'])
    def get_results(self):
        pk = self.kwargs[pk]
        queryset = Results.objects.filter(user_id=pk)
        return queryset





