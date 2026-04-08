from django.shortcuts import render, HttpResponse
import requests
import os
from dotenv import load_dotenv, dotenv_values
from .models import MCQstats, Question, Option
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

load_dotenv()

# Create your views here.

base_url = ""

@login_required(login_url='login_user')
def mcqHome(request):

    user = request.user

    top_stats = MCQstats.objects.order_by('-score')[:10]
    user_score = MCQstats.objects.get(user=user).score

    return render(request, "mcqPage.html", {"user_score" : user_score,
                                            "top_stats" : top_stats})

@login_required(login_url='login_user')
def dynamicQuestions(request):
    keywords = "malware OR hackers"
    language = "en"
    url = f"https://newsdata.io/api/1/latest?apikey={os.getenv('NEWS_API_KEY')}&q={keywords}&language={language}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        results = news_data.get('results')
        print(news_data)
    else:
        print(f"Failed to retreive data {response.status_code}")

    return render(request, "dynamicQuestions.html", {"news_data" : news_data})


@login_required(login_url='login_user')
def staticQuestions(request):

    questions_options = {}

    # select 5 random questions, if less than 5 questions available, retreieve all.
    if Question.objects.count() >= 5:
        questions = Question.objects.order_by('?')[:5]
    else:
        questions = Question.objects.all()

    for question in questions:
        options = Option.objects.filter(question=question)
        questions_options[question] = options

    return render(request, "staticQuestions.html", {"questions_options" : questions_options})


@login_required(login_url='login_user')
def submitStaticQuiz(request):
    score = 0
    total = 0

    for question, option in request.POST.items():

        if question.startswith("question_"):
            selected_option_id = option

            option = Option.objects.get(id=selected_option_id)

            if option.correct_option:
                score += 1
            
            total += 1
        
        user_stat, created = MCQstats.objects.get_or_create(user=request.user, defaults={"score" : 0, "questions_answered" : 0})


    user_stat.questions_answered += total
    user_stat.score += score
    user_stat.save()

    return HttpResponse(f"Your score: {score}/{total}")