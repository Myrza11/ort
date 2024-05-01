from rest_framework import serializers
from .models import *
from django.utils import timezone
from datetime import timedelta


class PassOrtTestSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()
    test_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        self.check_answer(validated_data)
        response = self.finalize_response(validated_data)
        self.record_resultAnalysis(validated_data)
        return response

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.objResult = None 
            self.Score = 0
            self.score2 = 0
    
    def check_answer(self, validated_data):
        result_id = self.context['pk']
        objResult = Results.objects.get(id=result_id)
        question_id = validated_data.get('question_id')
        question = Question.objects.filter(id=question_id).first()
        answer = validated_data.get('answer')

        if not question or answer is None:
            raise serializers.ValidationError('queston_id is not correct or answer is None')
        
        objanswers = Answer.objects.filter(question_id=question_id)
        objResultAnswer = ResultAnswer.objects.create(result_id=objResult, question_id=question)

        for objanswer in objanswers:
            if objanswer.answer != answer:
                objResultAnswer.is_correct = 'FALSE'
            else:
                objResultAnswer.is_correct = 'TRUE'
                self.Score += 1
                break
        objResultAnswer.save()

        return None
    
    def finalize_response(self, validated_data):
        result_id = self.context['pk']
        
        correct_answers = ResultAnswer.objects.filter(result_id=result_id, is_correct='TRUE').count()
        incorrect_answers = ResultAnswer.objects.filter(result_id=result_id, is_correct='FALSE').count()
        uncompleted_answers = ResultAnswer.objects.filter(result_id=result_id, is_correct='UNCOMPLETED').count()
        total_answers = correct_answers + incorrect_answers + uncompleted_answers
        score1 = self.Score
        score = (score1 * 100) / total_answers
        
        results = Results.objects.get(id=result_id)
        results.end_time = timezone.now()
        results.score = score
        results.save()

        end_time = results.end_time
        scheduled_end_time = results.scheduled_end_time

        if end_time > scheduled_end_time:
            results.score = 0
            results.save()
            raise serializers.ValidationError('Вы закончили тест не вовремя')

        return results
    
    def record_resultAnalysis(self, validated_data):
        result_id = self.context['pk']
        objResult = Results.objects.get(id=result_id)
        user = self.context['request'].user
        objTest = Test.objects.get(id=objResult.test_id.id)
        subject_id = objTest.subject_id
        objTopics = Topics.objects.filter(subject_id=subject_id)

        for objone in objTopics:

            try:
                objResultAnalysis = ResultAnalysis.objects.get(topic_id=objone, user_id=user, result_id=objResult)
            except ResultAnalysis.DoesNotExist:
                objResultAnalysis = ResultAnalysis.objects.create(topic_id=objone, user_id=user, result_id=objResult)

            objQuestion = Question.objects.filter(topic_id=objResultAnalysis.topic_id)
            objResultAnswers = ResultAnswer.objects.filter(result_id=objResult)

            objResultAnalysis.total_questions=len(objQuestion)
            objResultAnalysis.correct_answers = 0
            objResultAnalysis.save()

            for question in objResultAnswers:
                print('djn')
                print(question.is_correct)
                if question.is_correct == 'TRUE':
                    objResultAnalysis.correct_answers = objResultAnalysis.correct_answers + 1
            
            objResultAnalysis.save()
        return None



    class Meta:
        model = Results
        fields = "__all__"


class StartTestSerializer(serializers.ModelSerializer):
    test_id = serializers.IntegerField()

    
    def create_results(self, validated_data):
        test_id = validated_data.get('test_id')
        test = Test.objects.filter(id=test_id).first()
        if not test:
            raise serializers.ValidationError('This test id does not exist')
        
        user = self.context['request'].user
        objtest = Test.objects.get(id=test_id)

        start_time = timezone.now()
        duration = objtest.duretion
        scheduled_end_time = start_time + timedelta(minutes=duration.total_seconds() // 60)

        objResult = Results.objects.create(user_id=user, test_id=objtest, start_time=start_time, scheduled_end_time=scheduled_end_time)

        return objResult
    
    class Meta:
        model = Results
        fields = "__all__"
    

class GetSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class GetTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__' 


class GetQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__' 

class GetResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'