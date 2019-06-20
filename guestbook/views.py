from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import guestbook
from guestbook.models import Guestbook


def list(request):
    guestbooklist = Guestbook.objects.all().order_by('-id')
    data = {'guestbooklist': guestbooklist}
    return render(request, 'guestbook/list.html', data)


def deleteform(request):
    id = request.GET.get('id')
    print('deleteform id='+id)
    data = {'id' : id}

    return render(request, 'guestbook/deleteform.html',data)

def delete(request):
    id = request.POST['id']
    password = request.POST['password']
    print(id)
    post_instance = Guestbook.objects.get(id=id)
    if post_instance.password == password:
        post_instance.delete()

    return HttpResponseRedirect('/guestbook')


def add(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['contents']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')