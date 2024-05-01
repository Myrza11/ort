from datetime import timezone
from django.db import models
from register.models import CustomUser
from django.utils import timezone

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='subject_photo/')
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Topics(models.Model):
    HARD = 'HARD'
    MEDIOUM = 'MEDIOM'
    EASY = 'EASY'
    Level_Choises = [
        (HARD, 'HARD'),
        (MEDIOUM, 'MEDIOUM'),
        (EASY, 'EASY')]
    name = models.CharField(max_length=50)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='topics_photo/')
    description = models.TextField()
    quetion_type = models.CharField(max_length=20, choices=Level_Choises)

    def __str__(self):
            return self.name


class Question(models.Model):
    question_text = models.TextField()
    image = models.ImageField(upload_to='question/')
    topic_id = models.ForeignKey(Topics, on_delete=models.CASCADE)

    def __str__(self):
        return f'вопрос по {self.topic_id.name} {self.question_text}'


class Answer(models.Model):
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    CHOISE_CORRECT = [
        (TRUE, 'TRUE'),
        (FALSE, 'FALSE'),
    ]
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.CharField(max_length=10, choices=CHOISE_CORRECT)




class Test(models.Model):
    name = models.CharField(max_length=50)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    duretion = models.DurationField()

    def __str__(self):
        return self.name


class TestQuestion(models.Model):
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)


class Results(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    scheduled_end_time = models.DateTimeField(null=True, blank=True)
    

class ResultAnswer(models.Model):
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    UNCOPLATED = 'UNCOMPLETED'
    CHOISE_CORRECT = [
        (TRUE, 'TRUE'),
        (FALSE, 'FALSE'),
    ]
    result_id = models.ForeignKey(Results, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.CharField(max_length=10, choices=CHOISE_CORRECT, default=UNCOPLATED)


class ResultAnalysis(models.Model):
    topic_id = models.ForeignKey(Topics, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    result_id = models.ForeignKey(Results, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(null=True, blank=True)
    total_questions = models.IntegerField(null=True, blank=True)
    date_recorded = models.DateTimeField(default=timezone.now)