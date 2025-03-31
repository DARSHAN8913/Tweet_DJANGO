from django.shortcuts import render
from .forms import tweetform
from django.shortcuts import get_object_or_404,redirect

# Create your views here.
def index(request):
    return render(request,"index.html")

def tweet_list(request):
    tweets=tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

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

def tweet_edit(request,tweet_id):
    tweet_in=get_object_or_404(tweet,pk=tweet_id,
                               user=request.user)
    if request.method=='POST':
       form=tweetform(request.POST,request.FILES,
                      instance=tweet_in)
       if form.is_valid():
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')

    else:
        form=tweetform(instance=tweet_in)
    return render(request,'tweet_form.html',{'form':form})
    
def tweet_delete(request,tweet_id):
    tweet_in=get_object_or_404(tweet,pk=tweet_id,
                               user=request.user)
    if request.method=='POST':
        tweet_in.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',
                  {"Tweet":tweet_in}) 
         

