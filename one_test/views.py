from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import subprocess
import requests
import string

@csrf_exempt
def home(request):
    return render(request, 'one_test/home.html')

def filter_string(s):
    return ''.join(filter(lambda char: char in string.printable[:-3], s))

def submit_code(code, url):
    open('stdout', 'w').truncate()
    open('a.py', 'w').write(filter_string(code))
    subprocess.call(['cf', 'submit', '-f', 'a.py', url],
                    stdout=open('stdout', 'w'),
                    encoding='utf8')

def test_code(request, status={'answer': '', 'done': 1}):
    if request == None:
        next_out = open('stdout', 'r').read()
        if next_out:
            status['answer'] = filter_string(next_out)
        open('stdout', 'w').truncate()
        return status
    
    data = request.GET.dict()

    status['done'] = 0
    submit_code(data['code'], data['url'])
    status['done'] = 1

    return JsonResponse({}, status=200)

def get_status(request):
    return JsonResponse(test_code(None), status=200)

def get_task(request):
    url = request.GET.dict()['url']
    html = requests.get(url, headers={'Accept-Language': 'ru-RU'}).text;
    return JsonResponse({'html': html}, status=200)