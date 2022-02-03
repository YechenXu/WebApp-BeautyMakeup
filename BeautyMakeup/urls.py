from django.urls import path
from . import views
app_name = 'BeautyMakeup'
urlpatterns = [

    path('', views.home, name='beauty_makeup_home'),
    path('homeAlt', views.homeAlt, name='homeAlt'),
    path('item-list', views.beauty_makeup_list, name='beauty-makeup-list'),
    path('items/<int:item_id>', views.beauty_makeup_details, name="item-detail"),
    path('items/add-item', views.beautymakeup_add_item, name="add-item"),

    path('items/edit-item/<int:item_id>', views.beautymakeup_edit_item, name="edit-item"),
    path('items/edit-item/submit-edit/<int:item_id>', views.beautymakeup_submit_edit, name="submit-edit"),
    path('items/delete-item/<int:item_id>', views.beautymakeup_delete_item, name="delete-item"),
    # searchResults page
    path('search', views.item_search, name="item-search"),

    #comment view
    path('item-add', views.beauty_makeup_comment, name='beauty_makeup_comment'),
    #comment actions
    path('items/add-comment', views.new_comment_add, name="add-comment"),
    path('delete-comment', views.delete_comment, name="delete-comment"),
    path('edit-comment', views.edit_comment, name="edit-comment"),

    path('items/change-role', views.update_user_role, name="change-role"),

]