from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
# Create your views here.

# 대학명만 입력하면 첫번쨰 게시판으로 이동
def univ(request, univ):
    # try:
    _univ = get_object_or_404(Univ, name=univ)
    _ctgy = get_list_or_404(Category, univ = _univ)[0]
    # except Exception as ex:
    #     print(ex)
    #     return redirect(reverse('main'))

    return redirect(f'/{univ}/{_ctgy.name}')



# 대학명, 게시판 확인하고 이동
def read_Board(request, univ, category):
    # try:
    _univ = get_object_or_404(Univ, name=univ)
    _ctgy = get_object_or_404(Category, univ = _univ, name = category)
    # except Exception as ex:
    #     print(ex)
    #     return redirect(reverse('main'))
    
    ctx = {
        'queryset' : Post.objects.filter(ctgy=_ctgy),
        'categories' : Category.objects.filter(univ=_univ),
    }
    
    return render(request,'board/board.html', ctx)

def create_Post(request, univ, category):
    # try:
    _univ = get_object_or_404(Univ, name=univ)
    _ctgy = get_object_or_404(Category, univ = _univ, name = category)
    # except Exception as ex:
    #     print(ex)
    #     return redirect(reverse('main'))

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.author = request.user
            except:
                post.is_anonymous = True
            post.ctgy = _ctgy
            post.save()
            return redirect('board',post.ctgy.univ.name, post.ctgy.name)
    else:
        form = PostForm()

    return render(request, 'board/new_post.html', {'form': form})

def read_Post(request, univ, category, pk):
    # try:
    _univ = get_object_or_404(Univ, name=univ)
    _ctgy = get_object_or_404(Category, univ = _univ, name = category)
    _post = get_object_or_404(Post, ctgy=_ctgy, id=pk)
    # except Exception as ex:
    #     print(ex)
    #     return redirect(reverse('main'))

    ctx = {
        'post' : _post
    }
        
    return render(request, 'board/post_detail.html', ctx)
    
def create_Comment(request, univ, category, pk):

    # try:
    _univ = get_object_or_404(Univ, name=univ)
    _ctgy = get_object_or_404(Category, univ = _univ, name = category)
    _post = get_object_or_404(Post, ctgy=_ctgy, id=pk)
    # except Exception as ex:
    #     print(ex)
    #     return redirect(reverse('main'))

    content = request.POST.get('comment')

    if content != '':
        Comment.objects.create(post=_post,author=request.user,content=content)

    return redirect('read_Post',univ,category,pk)