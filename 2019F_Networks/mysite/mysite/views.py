from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import time

from mysite.models import Login


def index(request):
    if request.method == 'GET':
        uid = request.GET.get('id', None)
        if uid is not None:
            last = Login.objects.filter(user=uid).order_by('-date')
            return render(request, 'index.html', 
                          {'uid': uid, 'last': last[0]})
        else:
            return render(request, 'index.html')
    elif request.method == 'POST':
        uid = request.POST.get('id')
        date = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
        login = Login(user=uid,
                      date=date)
        login.save()
        return HttpResponseRedirect(f'/?id={uid}')

