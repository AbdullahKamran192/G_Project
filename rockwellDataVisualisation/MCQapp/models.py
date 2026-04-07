from django.db import models
from MAINapp.models import DjangoAdmin, User
from django.core.validators import MinValueValidator
from django.db.models import Q

# Create your models here.

class Question(models.Model):
    question = models.TextField()
    admin = models.ForeignKey(DjangoAdmin, on_delete=models.CASCADE)

    def __str__(self):
        return self.question 
    
class Option(models.Model):
    option_description = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    correct_option = models.BooleanField(default=False)

    def __str__(self):
        return self.option_description

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question'],
                condition=Q(correct_option=True),
                name='one_correct_option',
                violation_error_message = "There must only be one correct option per question"
            )
        ]

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

class UserAnswer(models.Model):
    is_correct = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['quiz', 'question'],
                name = 'one_answer_per_question_per_quiz'
            )
        ]


class MCQstats(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(0)])
    questions_answered = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE) # each user has only one row

    def __str__(self):
        return str(self.score)
