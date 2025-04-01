from django.shortcuts import render
from .forms import tweetform,UserRegistrationForm 
from .models import tweet
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login



# Create your views here.

def tweet_list(request):
    tweets=tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method=="POST":
       form=tweetform(request.POST,request.FILES)
       if form.is_valid():
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')

    else:
        form=tweetform()
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet_in=get_object_or_404(tweet,pk=tweet_id,
                               user=request.user)
    if request.method=='POST':
       form=tweetform(request.POST,request.FILES,
                      instance=tweet_in)
       if form.is_valid():
           tweet_ins=form.save(commit=False)
           tweet_ins.user=request.user
           tweet_ins.save()
           return redirect('tweet_list')

    else:
        form=tweetform(instance=tweet_in)
    return render(request,'tweet_form.html',{'form':form})
    
@login_required
def tweet_delete(request,tweet_id):
    tweet_in=get_object_or_404(tweet,pk=tweet_id,
                               user=request.user)
    if request.method=='POST':
        tweet_in.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',
                  {"Tweet":tweet_in}) 

# @login_required         
def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else: 
        form=UserRegistrationForm()

    return render(request,'registration/register.html',
                  {"form":form})

