from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
# from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import JsonResponse
from actions.models import Action


# Create your views here.

def profile(request, username):
    user = get_object_or_404(User, username=username)

    actions = Action.objects.filter(user_id=user.id).order_by('-date_created')[:5]

    return render(request,
                  "users/user/profile.html",
                  {"user":user, "actions":actions}
                  )


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        duplicate_user = user = User.objects.filter(username=username)
        if len(duplicate_user) == 0:
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            user = User.objects.create_user(username, email, password)
            user.details.role = role
            user.save()

            # User should immediately logged in when successfully register
            request.session['username'] = user.username
            request.session['role'] = user.details.role

            messages.add_message(request, messages.SUCCESS,
                             "You successfully registered with the username %s" % user.username)

            return redirect('BeautyMakeup:beauty_makeup_home')
        else:
             messages.add_message(request, messages.ERROR,
                                   "Username has been taken, try another")
    return render(request,
                  "users/user/register.html",
                  )

def login_user(request):
    username = request.POST.get("username")
    pw = request.POST.get("pw")
    user = authenticate(username=username, password=pw)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS,
                             "You successfully logged in successfully")
        return redirect('BeautyMakeup:beauty_makeup_home')
    else:
        messages.add_message(request, messages.ERROR,
                             "Invalid username or password")
        return redirect('BeautyMakeup:homeAlt')


def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('BeautyMakeup:homeAlt')



# link to edit profile page.
def edit_profile(request, username):
    user = User.objects.get(username=username)
    return render(request,
                  "users/user/editProfile.html",
                  {"user": user}
                  )


def submit_profile_edit(request, username):

    user = User.objects.get(username=username)

    if request.method == 'POST':
        # process the form

        firstname = request.POST.get("edit-firstname")
        lastname = request.POST.get("edit-lastname")
        email = request.POST.get("edit-email")

        # update information
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        # save update
        user.save()

        messages.add_message(request, messages.INFO, "You successfully edited %s's profile" %user.username)

        return redirect("users:profile", user.username)
    else:
        # messages.add_message(request, messages.WARNING, "Failed edit the item %s" %editing_item.title)
        return redirect("users:edit-profile", user.username)


def change_password(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        try:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
            new_password = request.POST.get('new_password')
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': 'success'}, status=200)
        except User.DoesNotExist:
          #  if user not exist
            return JsonResponse({'error': 'No user found with that username'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)

