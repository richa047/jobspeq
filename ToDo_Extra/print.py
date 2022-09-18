1.create todo project
2.to create default tables  use migrate ie python3 manage.py migrate
3.python3 manage.py createsuperuser
note -now u can access the admin panel
4.create app named tasks
5 in setting.py of project(inner folder) declare the app.
6.create urls.py in app
7.write code in view.py(tasks app) and
 write that path in urls.py(task app)
  then include this urls.py in 
  urls.py(todoa proj inner folder).
8.create template folder uner task app
9.create model
10 make migration,migrate,create superuser
11.register the model in admin.py(task app) so that you can see the table in admin panel
note once u see task on admin panel u have to reder it from there to the template.
12. use modal forms.
13 .In task app create modal form ie form.py
note- when we specify what model we want replicate it will go and create all form fields for us
14.once u have form import it in view and from view import it in template
---------------------------------------
proj structure
TODO(main proj folder)
tasks(app)
-migration
-template/tasks
-admin.py
-forms.py
-models.py
-urls.py
-views.py

todo(inner proj folder)
-settings.py
-urls.py
------------------------------------------------------------------
settings.py
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4el@z4%@%97s7929&%q4n^q#0**%&_7)ei&qamtijpqih2j^$@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'todo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'todo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

--------------------------------------
templates/tasks/list.html


<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

<style>

	body{
		background-color: #638CB8;
	}

	input{
		width: 100%;
		padding: 12px 20px;
		margin: 8px 0;
		box-sizing: border-box;
	}

	input::placeholder {
	  color: #d3d3d3;
	}

	.submit{
		background-color: #6BA3E8;
	}

	.center-column{
		width:600px;
		margin: 20px auto;
		padding:20px;
		background-color: #fff;
		border-radius: 3px;
		box-shadow: 6px 2px 30px 0px rgba(0,0,0,0.75);
	}

	.item-row{
		background-color: #906abd;
		margin: 10px;
		padding: 20px;
		border-radius: 3px;
		color: #fff;
		font-size: 16px;
		box-shadow: 0px -1px 10px -4px rgba(0,0,0,0.75);
	}

	.btn-danger{
		background-color: #ffae19;
		border-color: #e59400;
	}

</style>

<div class="center-column">

	<form method="POST" action="/">
		{% csrf_token %}
		{{form.title}}
		<input class="btn btn-info" type="submit" name="Create Task">
	</form>

	<div class="todo-list">

	{% for task in tasks %}
		<div class="item-row">
			<a class="btn btn-sm btn-info" href="{% url 'update_task' task.id %}">Update</a>
			<a class="btn btn-sm btn-danger" href="{% url 'delete' task.id %}">Delete</a>

			{% if task.complete == True %}
			<strike>{{task}}</strike>
			{% else %}
			<span>{{task}}</span>
			{% endif %}
		</div>
	{% endfor %}
	</div>
</div>


------------------
delete.html
<p> Are you sure want to delete"{{item}}"</p>

<a href="{% url 'list' %}">Cancel</a>
<form method ="POST" action="">
  {% csrf_token %}
  <input type ="submit" name ="Confirm">
</form>
-----------------------
update.html
<h3>Update Task</h3>

<form method="POST" action="">
	{% csrf_token %}

	{{form}}
	<input type="submit" name="Update Task">
	
	
</form>
---------------------------
urls.py(task)
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="list"),
	path('update_task/<str:pk>/', views.updateTask, name="update_task"),
	path('delete/<str:pk>', views.deleteTask, name ="delete"),
]
------------------------------------
views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *

# Create your views here.

def index(request):
	tasks = Task.objects.all()#atore  all the data to template

	form = TaskForm()

	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')


	context = {'tasks':tasks, 'form':form}#format dictionary type
	return render(request, 'tasks/list.html', context)

def updateTask(request, pk):
	task = Task.objects.get(id=pk)

	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}

	return render(request, 'tasks/update_task.html', context)

def deleteTask(request, pk):
	item = Task.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/')

	context = {'item':item}
	return render(request, 'tasks/delete.html', context)
--------------------------------------------------------------------------
urls.py(todo inner proj folder)

 from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]
--------------------------------------------------------------------------




---------------------------------


-migration
# Generated by Django 3.2.4 on 2021-08-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('complete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]