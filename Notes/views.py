from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Signup,Contact,Note
from django.contrib.auth import login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

#about 
def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')


def contact(request):
    error = ''
    # fullname,email,mobile,subject,message
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        subject = request.POST['subject']
        message = request.POST['message']
        
        try:
            Contact.objects.create(fullname=fullname,email=email,mobile=mobile,subject=subject,message=message,messagedate=date.today(),isread='no')
            error = 'no' 
        except: 
            error = 'yes'   
    return render(request,'contact.html')

def signup(request):
    error = ""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_home')
    if request.user.is_authenticated:
        return redirect('profile')
    
        
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        contact = request.POST['contact']
        email = request.POST['emailid']
        password = request.POST['password']
        branch = request.POST['branch']
        role = request.POST['role']
    try:
        user = User.objects.create_user(first_name=first_name,last_name=last_name,username=email,password=password)
        Signup.objects.create(user=user,contact=contact,branch=branch,role=role)
        error = 'no'
        
    except:
        error = 'yes'
    return render(request,'signup.html',locals())

def login_user(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['emailid']
        password = request.POST['pwd']
        user = authenticate(username=username,password=password)
        print(user.email)
        
    try:
        if user:
            print(user)
            login(request, user)
            error = 'no'
        else:
            error = 'yes'
            
    except:
        error = 'yes'
    
        
    return render(request,'login.html',locals())

def login_admin(request):
    error = ''
    user = None
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pwd']
        user = authenticate(username=username,password=password)
        print(user)
    try:
        if user is not None and user.is_staff:
            print(user)
            login(request, user)
            error = 'no'
        else:
            error = 'yes'
    except AttributeError:
        error = 'yes'
    return render(request,'login_admin.html',locals())

@login_required
def chanagepassword(request):
    error = ''
    if request.method == 'POST':
        currentpass = request.POST['old']
        newpass = request.POST['new']
        confirm_pass = request.POST['confirm']
        user = request.user
        try:
            if user.check_password(currentpass):
                user.set_password(newpass)
                user.save()
                error = 'no'
            else:
                error = 'not'
        except:
            error = 'yes'
    return render(request,'changepassword.html',locals())

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    #if user is logged in or not  
    user = User.objects.get(id=request.user.id)
    data = get_object_or_404(Signup,user = user)
    print(data)
    context = {
        'data':data,
        'user': user
    }
    return render(request,'profile.html',context)

@login_required
def edit_profile(request):
    user = get_object_or_404(User,id=request.user.id)
    data = get_object_or_404(Signup,user= user)
    error = False
    if request.method == 'POST':
        # firstname,lastname,contact,emailid,branch
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        contact = request.POST['contact']
        branch = request.POST['branch']
        user.first_name = firstname
        user.last_name = lastname
        data.contact = contact
        data.branch = branch
        user.save()
        data.save()
        error = True
    context  = {
        'user':user,
        'data':data,
        'error': error
    }    
    return render(request,'edit_profile.html',context)

@login_required
def admin_home(request):
    error = ''
    return render(request,'admin_home.html',locals())

@login_required
def change_passwordadmin(request):
    error = ''
    if request.method == 'POST':
        oldpass= request.POST['oldpassword']
        newpassword = request.POST['newpassword']
        confirmpassword = request.POST['confirmpassword']
     
        user = request.user
        try:
            if newpassword != confirmpassword:
              error = 'yes'
            elif user.check_password(oldpass):
                user.set_password(newpassword)
                user.save()
                error = 'no'
            else:
                error = 'not'
            
        except:
            error ='yes'
    return render(request,'change_passwordadmin.html',locals())

@login_required
def uploadNotes(request):
    error = ''
    if request.method == 'POST':
        # branch,subject,filetype,description,notesfile
        branch = request.POST['branch']
        subject = request.POST['subject']
        filetype = request.POST['filetype']
        description = request.POST['description']
        notesfile = request.FILES['notesfile']
        user = User.objects.filter(username=request.user.username).first()
        try:
            note = Note.objects.create(user=user,branch=branch,subject=subject,filetype=filetype,notesfile=notesfile,descriptions=description,uploading_date =date.today(),status='pending')
            error = 'no'
        except: 
            print('error as')
            error = 'yes' 
    
    return render(request,'upload_notes.html',locals())

@login_required
def view_mynotes(request):
    
    notes = Note.objects.filter(user=request.user)
    context = {
        'notes':notes
    }
    return render(request,'view_mynotes.html',locals())
@login_required
def delete_mynotes(reqest,id):
    note = get_object_or_404(Note,id=id)
    if note:
        note.delete()
    return redirect('view_mynotes')

@login_required
def view_all_note(request):
    error = ''
    try:
        notes = Note.objects.all()
        error = 'no'
    except:
        error = 'yes'
    return render(request,'viewallnotes.html',locals())

#admin panel work 
#pending_note,rejected_note,accepted_notes,all_notes 
@login_required
def pending_note(request):
    notes = Note.objects.filter(status='pending')
    context ={
        'notes':notes
    }
    return render(request,'pending_note.html',context)

@login_required
def assign_status(request,note_id):
    error = ''
    if request.method == 'POST':
        status = request.POST['status']
    try:
        notes = get_object_or_404(Note,id=note_id)
        print(notes)
        notes.status = status
        notes.save()
        error = 'no'
    except:
        error ='yes'
    context = {
        'notes':notes
    }
    return render(request,'assign_status.html',locals())

@login_required
def accepted_notes(request):
    notes = Note.objects.filter(status='Accept')
    return render(request,'accepted_notes.html',locals())

@login_required
def delete_notes(request,id):
    note = Note.objects.filter(id=id)
    if note:
        note.delete()
    return redirect('pending_note')
    

@login_required
def rejected_notes(request):
    notes = Note.objects.filter(status='Reject')
    context = {
        'notes':notes
    }
    return render(request,'rejected_notes.html',locals())
@login_required
def all_notes(request):
    notes = Note.objects.all()
    return render(request,'all_notes.html',locals())

@login_required
def view_queries(request,id):
    contact = get_object_or_404(Contact, id=id)
    contact.isread = 'yes'
    contact.save()
    return render(request,'view_queries.html',locals())
@login_required
def unread_queries(request):
    contact = Contact.objects.filter(isread= 'no')
    return render(request,'unread_queries.html',locals())

@login_required
def view_users(request):
    users = Signup.objects.all()
    return render(request,'view_users.html',locals())
@login_required
def delete_users(request,id):
    user = User.objects.filter(id=id)
    if user:
        user.delete()
        return redirect('view_users')
    return redirect('view_users',locals())
    

@login_required
def read_queries(request):
    contact = Contact.objects.filter(isread="yes")
        
    return render(request,'read_queries.html',locals())



def custom_not_found(request, exception):
    return render(request, '404.html', status=404)



