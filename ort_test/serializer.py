from rest_framework import serializers
from .models import *
from django.utils import timezone
from datetime import timedelta


class StartOrtTestSerializer(serializers.ModelSerializer):
    test_id = serializers.IntegerField()

    def create_results(self, validated_data):
        test_id = validated_data.get('test_id')
        test = Test.objects.filter(id=test_id).first()
        if not test:
            raise serializers.ValidationError('this test id does not exist')
        user = self.context['request'].user
        objtest = Test.objects.get(id=test_id)

        objResult = Results.objects.create(user_id=user, test_id=test_id)
        start_time = objResult.start_time
        duretion = objtest.duretion
        scheduled_end_time = start_time + timedelta(minutes=duretion)

        objResult.scheduled_end_time = scheduled_end_time
        objResult.save()

        return objResult
    
        
        

class PassOrtTestSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()
    test_id = serializers.IntegerField()
    user_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        self.create_results(validated_data)
        self.check_answer(validated_data)
        response = self.finalize_response(self.context['request'], None)
        return response

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.objResult = None 
            self.Score = 0

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
        self.objResult = objResult
        return objResult
    

    def check_answer(self, validated_data):
        print('jgchghfgcg')
        objResult = self.create_results(validated_data)
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
    
    def finalize_response(self, request, response, *args, **kwargs):
        # Получение данных о результате теста
        result_id = self.objResult.id

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
    

class PassTestSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()
    result_id = serializers.IntegerField()

    def check_answer(self, validated_data):
        question_id = validated_data.get('question_id')
        objResultid = validated_data.get('result_id')
        objResult = Results.objects.get(id=objResultid)
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
                break
        objResultAnswer.save()
        return objResultAnswer
    
    class Meta:
        model = ResultAnswer
        fields = "__all__"

class FinishTestSerializer(serializers.ModelSerializer):
    result_id = serializers.IntegerField()

    def finalize_response(self, validated_data):
        # Ваш код, который будет выполнен после завершения check_answer
        # response - это результат check_answer
        # request - запрос, который был отправлен
        result_id = validated_data.get('result_id')
        correctAnswers = ResultAnswer.objects.filter(result_id=result_id, is_correct='TRUE').count()
        incorrecttAnswers = ResultAnswer.objects.filter(result_id=result_id, is_correct='FALSE').count()
        uncompletedAnswers = ResultAnswer.objects.filter(result_id=result_id, is_correct='UNCOMPLETED').count()

        totalAnswers = correctAnswers + incorrecttAnswers + uncompletedAnswers
        total = (correctAnswers * 100) / totalAnswers
        results = Results.objects.get(id=result_id)

        results.end_time = timezone.now
        starttest = results.start_time
        endtest = results.end_time
        scheduled_end_time = results.scheduled_end_time
        print(scheduled_end_time.time() - endtest)
        if scheduled_end_time - endtest < 0:
            results.score = 0
            results.end_time = endtest
            results.save()
            raise serializers.ValidationError('вы закончили тест не вовремя')
        results.score = total
        results.save()
        return results
    
    class Meta:
        model = Results
        fields = ['result_id']