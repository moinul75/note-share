from django.urls import path
from django.conf.urls import handler404

from .views import *

# signup,login,login_admin
urlpatterns = [
    path('about/',about,name='about'),
    path('',index,name='index'),
    path('contact/',contact,name='contact'),
    path('signup/',signup,name='signup'),
    path('login/',login_user,name='login'),
    path('login_admin/',login_admin,name='login_admin'),
    path('profile/',profile,name='profile'),
    path('upload_notes/',uploadNotes,name='upload_notes'),
    path('view_mynotes/',view_mynotes,name='view_mynotes'),
    path('viewallnotes/',view_all_note,name='viewallnotes'),
    path('delete_mynotes/<str:id>/',delete_mynotes,name="delete_mynotes"),
    path('logout/',logout_view,name='logout'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('changepassword/',chanagepassword,name='changepassword'),
    path('admin_home/',admin_home,name='admin_home'),
    path('pending_note/',pending_note,name='pending_notes'),
    path('assign_status/<str:note_id>/',assign_status,name="assign_status"),
    path('delete_notes/<str:id>/',delete_notes,name="delete_notes"),
    path('accepted_notes/',accepted_notes,name='accepted_notes'),
    path('rejected_notes/',rejected_notes,name='rejected_notes'),
    path('all_notes/',all_notes,name='all_notes'),
    path('view_queries/<str:id>/',view_queries,name='view_queries'),
    path('view_users/',view_users,name='view_users'),
    path('unread_queries/',unread_queries,name='unread_queries'),
    path('read_queries/',read_queries,name='read_queries'),
    path('change_passwordadmin/',change_passwordadmin,name='change_passwordadmin'),
    path('delete_users/<str:id>/',delete_users,name='delete_users'),
    
]

#handle the 404 page in custom 
handler404 = 'Notes.views.custom_not_found'




