from django.shortcuts import render, redirect
from .models import BeautyMakeupItem, Comment, User
from actions.models import Action
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
import requests
import json

# Create your views here.

# home view
def home(request):
    items = BeautyMakeupItem.objects.all().order_by('-date_posted')
    if request.session.get("username", False):
        user = User.objects.get(username=request.session.get("username"))

        # filter the feeds that are related to the current user
        user_upload = BeautyMakeupItem.objects.all().filter(user_id=user.id)
        actions_user = Action.objects.all().filter(user_id=user.id)
        actions_target_user = Action.objects.all().filter(target_id=user.id,target_ct=ContentType.objects.get_for_model(User))
        action_target_item = Action.objects.all().filter(target_id__in=user_upload, target_ct=ContentType.objects.get_for_model(BeautyMakeupItem))

        actions = actions_user|actions_target_user|action_target_item
        actions = actions.order_by("-date_created")[:5]

        return render(request,
                      "BeautyMakeup/beauty_makeup/home.html",
                      {"items": items, "actions": actions}
                      )
    else:
        return render(request,
                      "BeautyMakeup/beauty_makeup/homeNoLogin.html",
                      {"items": items}
                      )


def homeAlt(request):
    return render(request, "BeautyMakeup/beauty_makeup/homeNoLogin.html")

# Item deatils view
def beauty_makeup_details(request, item_id):
    item = BeautyMakeupItem.objects.get(id=item_id)
    comments = Comment.objects.filter(item_id=item_id).order_by('-date_posted')
    return render(request,
                  "BeautyMakeup/beauty_makeup/details.html",
                  {"item": item, "comments": comments}
                  )

# item list view
def beauty_makeup_list(request):
    items = BeautyMakeupItem.objects.all().order_by('-date_posted')
    actions = Action.objects.all()
    return render(request,
              "BeautyMakeup/beauty_makeup/list.html",
              {"items": items, "actions": actions}
              )

# comment view
def beauty_makeup_comment(request):
    return render(request,
                  "BeautyMakeup/beauty_makeup/comment.html"
                  )

# search item from database using search query
def item_search(request):
    if request.method == 'GET':
        search_query = request.GET['search1']

    # search results contains a list of item that
    search_results = BeautyMakeupItem.objects.filter(title__icontains=search_query)
    return render(request,
                  "BeautyMakeup/beauty_makeup/searchResults.html",
                  {"items": search_results}
                  )


# add new item view
def beautymakeup_add_item(request):
    # redirect if not logged in
    if not request.session.get("username", False):
        return redirect('BeautyMakeup:homeAlt')

    if request.method == 'POST':
        # process the form
        title = request.POST.get("add-title")
        price = request.POST.get("add-price")
        condition = request.POST.get("add-condition")
        description = request.POST.get("description")
        availability = request.POST.getlist("add-availability")
        item_img = request.FILES["item_image"]

        # check the from content.
        # check if the content are only space.
        if title.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The title is invalid/empty, please try again.")
            return redirect("BeautyMakeup:add-item")

        if condition.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The condition is invalid/empty, please try again.")
            return redirect("BeautyMakeup:add-item")

        if description.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The description is invalid/empty, please try again.")
            return redirect("BeautyMakeup:add-item")

        # get the value of checkbox and re-construct them
        option = '/'.join(availability)
        if option == '':
            messages.add_message(request, messages.ERROR,"Please select at least one availability option.")
            return redirect("BeautyMakeup:add-item")

        # Detect the content of image using Microsoft Azure Computer Vision AI Service
        endpoint = "https://beautymakeupvision.cognitiveservices.azure.com/vision/v3.1/analyze"
        parameters = {
            'visualFeatures': 'Adult'
        }
        headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': 'cd660ada0be040f5a3b097fd08f89139',
        }
        response = requests.post(endpoint, headers=headers, params=parameters, data=item_img)
        result = response.json()

        # Handle API error message.
        if response.status_code != 200 and response.status_code != 201:
            messages.add_message(request, messages.ERROR,
                                 "%s" % result["message"])
            return redirect("BeautyMakeup:add-item")

        # warn user with corresponding error
        if result['adult']['isAdultContent']:
            messages.add_message(request, messages.ERROR,
                                 "Your image contains adult content,please change it.")
            return redirect("BeautyMakeup:add-item")

        if result['adult']['isRacyContent']:
            messages.add_message(request, messages.ERROR,
                                 "Your image contains racy content,please change it.")
            return redirect("BeautyMakeup:add-item")

        if result['adult']['isGoryContent']:
            messages.add_message(request, messages.ERROR,
                                 "Your image contains gory content,please change it.")
            return redirect("BeautyMakeup:add-item")

        user = User.objects.get(username=request.session.get("username"))

        new_item = BeautyMakeupItem(
            title=title,
            price = price,
            condition = condition,
            description = description,
            availability= option,
            author=request.session.get('username'),
            user=user,
            item_img = item_img
        )
        new_item.save()

        action = Action(
            user=user,
            verb="created the new item",
            target=new_item
        )
        action.save()

        messages.add_message(request, messages.SUCCESS, "You successfully submitted the new item: %s" %new_item.title )

        return redirect("BeautyMakeup:item-detail", new_item.id)

    else:
        # show the form
        # messages.add_message(request, messages.WARNING, "Failed add the item, try add again")
        return render(request,
                      "BeautyMakeup/beauty_makeup/add.html",
                      )


def beautymakeup_edit_item(request, item_id):
    editing_item = BeautyMakeupItem.objects.get(id=item_id)

    return render(request,
                  "BeautyMakeup/beauty_makeup/edit.html",
                  {"item": editing_item}
                  )


# Edit item view
def beautymakeup_submit_edit(request, item_id):

    if not request.session.get("username", False):
        return redirect('BeautyMakeup:homeAlt')

    editing_item = BeautyMakeupItem.objects.get(id=item_id)

    if request.method == 'POST':
        # process the form

        title = request.POST.get("add-title")
        price = request.POST.get("add-price")
        condition = request.POST.get("add-condition")
        description = request.POST.get("description")
        availability = request.POST.getlist("add-availability")

        # Check if the submit content are valid.
        if title.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The title is invalid/empty, please try again.")
            return redirect("BeautyMakeup:edit-item", item_id)

        if condition.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The condition is invalid/empty, please try again.")
            return redirect("BeautyMakeup:edit-item", item_id)

        if description.strip() == '':
            messages.add_message(request, messages.ERROR,
                                 "The description is invalid/empty, please try again.")
            return redirect("BeautyMakeup:edit-item", item_id)

        option = '/'.join(availability)
        if option == '':
            messages.add_message(request, messages.ERROR,
                                 "Please select at least one availability option.")
            return redirect("BeautyMakeup:edit-item", item_id)

        # update information
        editing_item.title = title
        editing_item.price = price
        editing_item.condition = condition
        editing_item.description = description
        editing_item.availability = option

        # save update
        editing_item.save()

        user = User.objects.get(username=request.session.get("username"))
        # log the action
        action = Action(
            user=user,
            verb="edited the item",
            target=editing_item
        )
        action.save()

        messages.add_message(request, messages.INFO, "You successfully edited the item %s" %editing_item.title)

        return redirect("BeautyMakeup:item-detail", item_id)
    else:
        # messages.add_message(request, messages.WARNING, "Failed edit the item %s" %editing_item.title)
        return redirect("BeautyMakeup:item-detail", item_id)



def beautymakeup_delete_item(request, item_id):
    # check if user logged in
    if not request.session.get("username", False):
        return redirect('BeautyMakeup:homeAlt')

    title = BeautyMakeupItem.objects.get(pk=item_id).title

    BeautyMakeupItem.objects.get(pk=item_id).delete()
    messages.add_message(request, messages.WARNING, "You successfully deleted the item %s" %title)
    return redirect("BeautyMakeup:beauty-makeup-list")

def new_comment_add(request):
    if not request.session.get("username", False):
        return redirect('BeautyMakeup:homeAlt')

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        commentTitle = request.POST.get('title')
        commentText = request.POST.get('comment')
        item_id = request.POST.get('item_id')
        user = User.objects.get(username=request.session.get("username"))

        # Check the content of the submitted form.
        if commentTitle =='':
            return JsonResponse({'error': 'Comment title is required.'}, status=200)
        elif commentText =='':
            return JsonResponse({'error': 'Comment is required.'}, status=200)

        try:
            item = BeautyMakeupItem.objects.get(pk=item_id)

            new_comment = Comment(
                author=request.session.get('username'),
                user=user,
                commentTitle=commentTitle,
                commentText=commentText,
                item=item
            )
            new_comment.save()

            # log the action
            action = Action(
                user=user,
                verb="added a new comment for item",
                target= item
            )
            action.save()

            # Find how many comment left for this item
            comment_length = Comment.objects.filter(item_id=item.id).count()

            return JsonResponse({'success':'success',"comment_length":comment_length,"comment_id":new_comment.id}, status=200)
        except BeautyMakeupItem.DoesNotExist:
            return JsonResponse({'error':'No item found with item ID.'}, status=200)

    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)


# Only admin could change other user's role
def update_user_role(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        new_role = request.POST.get('new_role')
        user.details.role = new_role
        user.save()

        # If the admin changed himself/herself'r role, then change the session's role
        if(username == request.session.get("username")):
            request.session['role'] = user.details.role

        action_user = User.objects.get(username=request.session.get("username"))
        # log the action
        action = Action(
            user= user,
            verb="'s role has been changed to "+new_role + " by administrator ",
            target = action_user
        )
        action.save()

        return JsonResponse({'success':'success','currentRole':request.session['role']},status=200)
    else:
        return JsonResponse({'error':'Invalid Ajax request'}, status=400)


def delete_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        item = comment.item

        user = User.objects.get(username=request.session.get("username"))
        action = Action(
            user=user,
            verb="just deleted a comment for item ",
            target = item
        )
        action.save()
        comment.delete()

        # Find how many comment left for this item
        comment_length = Comment.objects.filter(item_id=item.id).count()

        return JsonResponse({'success': 'success',"comment_length":comment_length}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)


def edit_comment(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    print(is_ajax)

    if is_ajax and request.method == "POST":
        comment_id = request.POST.get('comment_id')
        updated_title = request.POST.get('updated_title')
        updated_content = request.POST.get('updated_content')
        comment = Comment.objects.get(id=comment_id)
        comment.commentTitle = updated_title
        comment.commentText = updated_content
        comment.save()

        user = User.objects.get(username=request.session.get("username"))
        action = Action(
            user=user,
            verb="edited the comment for item ",
            target=comment.item
        )
        action.save()

        return JsonResponse({'success': 'success'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)





