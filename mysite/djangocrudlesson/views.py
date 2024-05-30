from django.shortcuts import render, redirect
from .models import Gender, User
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def index_gender(request):
    genders =Gender.objects.all() # SELECT * FROM GENDERS

    context = {
        'genders': genders 
    }
    return render(request, 'gender/index.html', context )

def create_gender(request):
    return render(request, 'gender/create.html')

def store_gender(request):
    gender = request.POST.get('gender')
    Gender.objects.create(gender=gender)
    messages.success(request, 'Gender successfully saved!')

    return redirect('/genders')


def show_gender(request, gender_id):
    gender = Gender.objects.get(pk=gender_id) 

    context = {
        'gender':  gender,
    }

    return render(request, 'gender/edit.html', context)

def edit_gender(request, gender_id):
    gender = Gender.objects.get(pk=gender_id) 

    context = {
        'gender':  gender,
    }

    return render(request, 'gender/edit.html', context)

def update_gender(request, gender_id):
    gender = request.POST.get('gender')
 
    Gender.objects.filter(pk=gender_id).update(gender=gender) # UPDATE GENDERS SET  GENDER = GENDER  WHERE GENDER_ID = GENDER_ID
    messages.success(request, 'Gender successfully updated')

    return redirect('/genders')


def delete_gender(request, gender_id):
    gender = Gender.objects.get(pk=gender_id) # SELECT * FROM GENDERS WHERE GENDER_ID = GENDER_ID

    context = {
        'gender':  gender,
    }

    return render(request, 'gender/delete.html', context)

def destroy_gender(request, gender_id):
    Gender.objects.filter(pk=gender_id).delete() #  DELETE FROM genders WHERE gender_id = gender_id
    messages.success(request, 'Gender successfully updated.')

    return redirect('/genders')

def index_user(request):
    users = User.objects.select_related('gender') # SELECT * FROM users  LEFT JOIN on users.gender_id = gender_id
    
    context = {
        'users': users,
    }
    return render(request, 'user/index.html', context)

def create_user(request):
    genders = Gender.objects.all()# select from genders

    context = {
        'genders': genders
    }

    return render(request, 'user/create.html', context) 

def store_user(request):
    firstName = request.POST.get('first_name')
    middleName = request.POST.get('middle_name')
    lastName = request.POST.get('last_name')
    age = request.POST.get('age')
    birthDate = request.POST.get('birth_date')
    genderId = request.POST.get('gender_id')
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirm_password')

    if password == confirmPassword:
        encryptedPassword = make_password('confirm_ password')
        User.objects.create(first_name=firstName,  middle_name=middleName, last_name=lastName, age=age, birth_date=birthDate, gender_id=genderId, username=username, password=encryptedPassword)

        messages.success(request, 'User successfully saved.')
        
        return redirect('/')
    else:
        messages.error(request, 'Password do not match. ')
        return render(request, 'user/create.html')
    
    

def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    
    context = {
        'user': user,
    }
    return render(request, 'user/delete.html', context)

def destroy_user(request, user_id):
    user = User.objects.filter(pk=user_id).values("first_name")
    if user.exists():
        first_name = user.first()["first_name"]
    else:
        first_name = "Uknown"
    User.objects.filter(pk=user_id).delete()

    messages.success(request, f'The user named {first_name} has been deleted.')
    return redirect("/")

def edit_user(request, user_id):
    user = User.objects.select_related("gender").get(pk=user_id)
    context = {'user': user}
    return render(request, 'user/edit.html', context)

def update_user(request, user_id):
    firstName = request.POST.get('first_name')
    middleName = request.POST.get('middle_name')
    lastName = request.POST.get('last_name')
    age = request.POST.get('age')
    birthDate = request.POST.get('birth_date')
    username = request.POST.get('username')
    gender = request.POST.get('gender')
    gender_id = User.objects.select_related("gender").values("gender_id").first()["gender_id"]
    User.objects.filter(pk=user_id).update(first_name=firstName, middle_name=middleName, last_name=lastName, age=age, birth_date=birthDate, username=username)
    Gender.objects.filter(pk=gender_id).update(gender=gender)
    
    messages.success(request, 'User successfully updated.')
    
    return redirect("/")

def show_user(request, user_id):
    user = User.objects.select_related('gender').get(pk=user_id)

    context = {
        'user': user,
    }

    return render(request, 'user/show.html', context)



