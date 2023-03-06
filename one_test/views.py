from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import subprocess

@csrf_exempt
def home(request):
    return render(request, 'one_test/home.html')

def test_code(request, status={'answer': '', 'done': 1}):
    if request == None:
        next_out = open('stdout', 'r').read()
        if next_out:
            status['answer'] = next_out[next_out.find('\n'):]
        open('stdout', 'w').truncate()
        return status
    data = request.GET.dict()
    if request.method == 'GET' and 'code' in data and status['done'] == 1:
        status['done'] = 0

        open('stdout', 'w').truncate()
        open('a.py', 'w').write(data['code'])
        subprocess.call(['cf', 'submit', '-f', 'a.py', 'https://codeforces.com/contest/1186/problem/A'],
                        stdout=open('stdout', 'w'),
                        encoding='utf8')
        
        status['done'] = 1
    return JsonResponse({}, status=200)

def get_status(request):
    return JsonResponse(test_code(None), status=200)
