from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    posts = Post.objects
    return render(request, 'blog/home.html', {'posts':posts})

@login_required
def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post_detail, 'form':form,})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.datetime.now()
            post.save()
            return redirect('detail', post_id=post.pk)
        
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form':form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.datetime.now()
            post.save()
            return redirect('detail', post_id = post.pk)
    
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('home')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    return redirect('detail', post_id=post.pk)


@login_required
def comment_delete(request,comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)
    post = comment.post
    comment.delete()
    return redirect('detail', post_id=post.id)


@login_required
def post_like(request, comment_id, ) :
    # 코멘트 정보 받아옴
    comment = get_object_or_404(Comment, pk=comment_id)
    post = comment.post
    # post = get_object_or_404(Post, pk=post_id)
    # 사용자가 로그인 된건지 확인
    if not request.user.is_active:
        return redirect('detail', post_id=post.id)    

    #사용자 정보 받아옴
    user = User.objects.get(username=request.user)
    comment.likes.add(user)
    print(comment.likes.filter(id=user.id).exists())
    print(comment.likes.count())

    count = comment.likes.count()
    
    # print(Comment.objects.filter(like=request.user.id).exists())
    if comment.likes == user: # 이 댓글에 지금 로그인한 사용자가 좋아요 누른 적 있으면
        print(aa)

    #좋아요에 사용자가 존재하면
    # if comment.likes.filter(id = request.user.id).exists():
        # 사용자를 지움
        # comment.likes.remove(user)
    # else:
    #     # 아니면 사용자를 추가
    #     comment.likes.add(user)
    #포스트로 리디렉션
    return redirect('detail', post_id=post.id,)
     #우리는 코멘트를 가져와서 거기다가 좋아요 기능을 만들건데
    # 코멘트마다 뭐를 하나씩 클릭하면
    # 코멘트 밑에 있는 숫자가 올라가겠끔만 하면 됨!!! 