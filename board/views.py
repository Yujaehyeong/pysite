from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User


def list(request):
    boardlist = Board.objects.all().order_by('-groupno', 'orderno')
    data = {'boardlist': boardlist}
    return render(request, 'board/list.html', data)


def writeform(request):
    if request.session._session:
        if request.method == 'GET':
                # if request.GET.get('groupno') is not None :
                #     data = {'groupno': request.GET.get('groupno'), 'orderno': request.GET.get('orderno'),\
                #             'depth': request.GET.get('depth')}
                #     return render(request, 'board/write.html', data)
            return render(request, 'board/write.html')
        else:
            data = {'groupno': request.POST['groupno'], 'orderno': request.POST['orderno'],\
                    'depth': request.POST['depth']}
            return render(request, 'board/write.html', data)
    return HttpResponseRedirect('/user/loginform')


def write(request):
    # user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    userid= request.session['authUser']['id']
    user = User.objects.get(id=userid)
    board.user = user


    if request.POST['groupno'] != '':
        print('request.POST[groupno] !=')
        board.groupno = request.POST['groupno']
        board.depth = int(request.POST['depth'])+1
        board.orderno = int(request.POST['orderno'])+1
    else :
        max_board = Board.objects.aggregate(max_groupno=Max('groupno'))
        if max_board is not None:
            max_groupno = 0 if max_board['max_groupno'] is None else max_board["max_groupno"]
            board.groupno = max_groupno + 1
        else :
            board.groupno = 1

    board.save()

    return HttpResponseRedirect('/board')

def updateform(request):
    boardid = request.GET.get('id')
    board = Board.objects.get(id=boardid)

    data = {
        'board' : board
    }

    return render(request, 'board/modify.html', data)

def update(request):
    boardid = request.POST['id']
    title = request.POST['title']
    content = request.POST['content']

    result = Board.objects.filter(id=boardid).\
        update(title = title, content=content)

    return HttpResponseRedirect('/board/view?id='+ boardid)

def view(request):
    board = Board.objects.get(id=request.GET.get('id'))

    data = {
        'board' : board
    }

    return render(request, 'board/view.html', data)

def delete(request):
    id = request.POST['id']
    board = Board.objects.get(id=id)
    board.delete()

    return HttpResponseRedirect('/board')