from django.shortcuts import render, HttpResponse
import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# Create your views here.

base_url = ""

def mcqHome(request):
    keywords = "malware OR hackers"
    language = "en"
    url = f"https://newsdata.io/api/1/latest?apikey={os.getenv('NEWS_API_KEY')}&q={keywords}&language={language}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        print(news_data)
    else:
        print(f"Failed to retreive data {response.status_code}")

    return render(request, "mcqPage.html")