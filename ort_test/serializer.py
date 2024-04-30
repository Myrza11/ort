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
        return response

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.objResult = None 
            self.Score = 0
    
    def check_answer(self, validated_data):
        print('jgchghfgcg')
        result_id = self.context['pk']
        print(result_id)
        print('hello')
        #result_id = validated_data.get('result_id')
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
                objResultAnswer.FALSE
            else:
                objResultAnswer.TRUE
                self.Score += 1
                break
        objResultAnswer.save()

        return None
    
    def finalize_response(self, validated_data):
        # Получение данных о результате теста
        result_id = self.context['pk']

        correct_answers = ResultAnswer.objects.filter(result_id=result_id, is_correct='TRUE').count()
        incorrect_answers = ResultAnswer.objects.filter(result_id=result_id, is_correct='FALSE').count()
        uncompleted_answers = ResultAnswer.objects.filter(result_id=result_id, is_correct='UNCOMPLETED').count()
        total_answers = correct_answers + incorrect_answers + uncompleted_answers
        #score = (correct_answers * 100) / total_answers
        score = self.Score
        print(score)

        # Обновление информации о результате теста
        results = Results.objects.get(id=result_id)
        results.end_time = timezone.now()
        results.score = score
        results.save()

        # Проверка, превысил ли пользователь запланированное время
        start_time = results.start_time
        end_time = results.end_time
        scheduled_end_time = results.scheduled_end_time

        if end_time > scheduled_end_time:
            results.score = 0
            results.save()
            raise serializers.ValidationError('Вы закончили тест не вовремя')

        return results

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