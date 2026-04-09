from django.urls import path
from . import views


urlpatterns = [
    path("", views.mcqHome, name="mcqHome"),
    path("dynamicquestions/", views.dynamicQuestions, name='dynamicQuestions'),
    path("staticquestions/", views.staticQuestions, name='staticQuestions'),
    path("submitstaticquiz/", views.submitStaticQuiz, name='submitStaticQuiz'),
    path("dynamicquestionsubmit/", views.dynamicQuestionSubmit, name='dynamicQuestionSubmit')
]