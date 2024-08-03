from django.db import models

## STRAIGHT COPY FROM STEAM QUIZ, FOR NOW I DON'T USE THIS METHOD TO STORE INFO.
class Quiz(models.Model):
    status = models.CharField(max_length=255)
    qstn_count = models.IntegerField()
    qstn_id = models.CharField(max_length=255)

    def __str__(self):
        return self.qstn_id

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    def __str__(self):
        return self.question

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option = models.CharField(max_length=255)
    def __str__(self):
        return self.option