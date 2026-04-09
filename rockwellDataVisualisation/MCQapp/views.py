from django.shortcuts import render, HttpResponse
import requests
import os
from dotenv import load_dotenv, dotenv_values
from .models import MCQstats, Question, Option
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
import string, json
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('AI_KEY'))

# Create your views here.

def get_article_text(url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = BeautifulSoup(response.text, "html.parser")

        article = data.find("article")

        if not article:
            article = data.find("div", class_="content") or data.find("div", class_="article-body") or data.find("div", class_="main-content")
        
        if not article:
            return "Could not find article text"
        
        paragraphs = article.find_all("p")

        text = ""

        for p in paragraphs:
            text += p.get_text(strip=True) + "\n"

        translator = str.maketrans('', '', string.punctuation)

        clean_text = text.translate(translator)
        clean_text = clean_text.replace("\n", " ")
        clean_text = " ".join(clean_text.split())
        
        return clean_text

    except Exception as e:
        return f"Error: {e}"


sample_dynamic_questions_data = [
    {
    "question" : "This is question 1",
    "options" : ["option 1", "option 2", "option 3", "option 4"],
    "correct_option" : "option 2"
    },
    {
    "question" : "This is question 2",
    "options" : ["option 1", "option 2", "option 3", "option 4"],
    "correct_option" : "option 1"
    },
    {
    "question" : "This is question 3",
    "options" : ["option 1", "option 2", "option 3", "option 4"],
    "correct_option" : "option 4"
    },
    {
    "question" : "This is question 4",
    "options" : ["option 1", "option 2", "option 3", "option 4"],
    "correct_option" : "option 4"
    },
    {
    "question" : "This is question 5",
    "options" : ["option 1", "option 2", "option 3", "option 4"],
    "correct_option" : "option 1"
    },
]

base_url = ""

@login_required(login_url='login_user')
def mcqHome(request):

    user = request.user

    top_stats = MCQstats.objects.order_by('-score')[:10]
    user_score = MCQstats.objects.get(user=user).score
    user_questions_answered = MCQstats.objects.get(user=user).questions_answered

    return render(request, "mcqPage.html", {"user_score" : user_score,
                                            "top_stats" : top_stats,
                                            "user_questions_answered" : user_questions_answered,
                                            "user_name" : user.username})

@login_required(login_url='login_user')
def dynamicQuestions(request):

    questions = []
    correct_answers = [] 

    for question_data in sample_dynamic_questions_data:
        questions.append({
            "question" : question_data["question"],
            "options" : question_data["options"],
            "article_link" : "https://www.google.com/"
        })

        correct_answers.append(question_data["correct_option"])
    
    request.session['correct_answers'] = correct_answers


    return render(request, "dynamicQuestions.html", {"questions_options" : questions})

@login_required(login_url='login_user')
def dynamicQuestionSubmit(request):
    award_points = 5

    correct_answers = request.session.get("correct_answers", [])
    score_total = 0

    for i, correct in enumerate(correct_answers):
        selected = request.POST.get(f"question_{i}")

        if selected == correct:
            score_total += award_points
    
    user_stat = MCQstats.objects.get(user=request.user)
    user_stat.score += score_total
    user_stat.questions_answered += len(correct_answers)
    user_stat.save()

    return render(request, "dynamicQuizResults.html", { "score" : score_total, "total": len(correct_answers) * 5})




    points_awarded = 2
    selected = request.POST.get("selected_option")
    correct = request.session.get("correct_option")
    result = ""

    if selected == correct:
        user_stat = MCQstats.objects.get(user=request.user)
        user_stat.score += 2
        user_stat.questions_answered += 1
        user_stat.save()
        result = "CORRECT! 2 points awarded."
    else:
        user_stat = MCQstats.objects.get(user=request.user)
        user_stat.questions_answered += 1
        user_stat.save()
        result = "WRONG!!"

    return render(request, "dynamicQuizResults.html", {"result" : result})


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