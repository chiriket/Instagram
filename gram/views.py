from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Image,Profile,Comments
from .forms import SignupForm, ImageForm, ProfileForm, CommentForm
from .email import send_welcome_email
from django.contrib.auth import login, authenticate

import datetime as dt


def index(request):
    profile = Profile.objects.all()
    images = Image.get_all_images()
    return render(request, 'index.html', {'images':images,"profile":profile})

# Create your views here.
# def index(request):
#     title = 'Home'
#     date = dt.date.today()
#     photos = Image.objects.all()
#     profiles = Profile.objects.all()
#     # print(profiles)
#     form = CommentForm()
#     return render(request, 'index.html', {'title':title, "photos":photos, "profiles":profiles, "form":form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Instagram account.'
            message = render_to_string('active.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def comment(request):
    #Getting comment form data
    if request.method == 'POST':
        image = get_object_or_404(Image, pk = image_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()
    return render(request, 'comments.html')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for confirming email. Now login to your account')
    else:
        return HttpResponse('Activation link is invalid')

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile/edit_profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form})


@login_required(login_url='/accounts/login')
def single_image(request, image_id):
    image = Image.get_image_id(image_id)
    comments = Comments.get_comments_by_images(image_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect('single_image', image_id=image_id)
    else:
        form = CommentForm()
        
    return render(request, 'image.html', {'image':image, 'form':form, 'comments':comments})
    
    

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username=search_term)
        message = f"{search_term}"
        profiles=  Profile.objects.all( )
        
        return render(request, 'search.html',{"message":message,"users": searched_users,'profiles':profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

def image(request,image_id):
    try:
        image = Image.objects.get(id = image_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,'image.html',{'image':image})

# def profile(request,id):
#     profile = Profile.objects.get(user_id=id)
#     post=Image.objects.filter(user_id=id)
                       
#     return render(request,'profile.html',{"profile":profile,"post":post})


# def profile(request):
#     date = dt.date.today()
#     current_user = request.user
#     # profile = Profile.objects.get(user=current_user.id)
#     # print(profile.profile_pic)
#     # posts = Image.objects.filter(user=current_user)
#     # images = Image.get_profile_images(profile.id)
#     # title = f'@{profile.username} Instagram photos and videos'
#     if request.method == 'POST':
#         signup_form = EditForm(request.POST, request.FILES,instance=request.user.profile) 
#         if signup_form.is_valid():
#            signup_form.save()
#     else:        
#         signup_form =SignupForm() 

#     # try:
#     #     images = Image.get_all_images(profile.id)
#     # except expression as identifier:
#     #     images = Image.get_profile_images(profile.id)
    
#     return render(request, 'profile/profile.html', {"date": date, "form":signup_form,"profile":profile})

def profile(request):
    profile = User.objects.get()
    # print(profile.id)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile.username} Instagram photos and videos'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details, 'images':images})

@login_required(login_url='/accounts/login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user
            # print(f'image is {upload.image}')
            upload.save()
            return redirect('profile')
            
    else:
        form = ImageForm()
    
    return render(request, 'profile/upload_image.html', {'form':form})

# @login_required(login_url='/accounts/login')
# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             upload = form.save(commit=False)
#             # upload.profile = request.user
#             # print(f'image is {upload.image}')
#             upload.save()
#             return redirect('profile', username=request.user)
#             return redirect('profile')
#     else:
#         form = ImageForm()
    
#     return render(request, 'profile/upload_image.html', {'form':form})