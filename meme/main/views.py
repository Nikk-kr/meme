from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import registerUser, loginUser
from django.contrib.sessions.backends.db import SessionStore # For session storage

import psycopg2
import requests
import bcrypt

s = SessionStore()

# connection to database

try:
    connection = psycopg2.connect(
        host = '127.0.0.1',
        port = '5432',
        database = 'memestore',
        user = 'postgres',
        password = 'Nikhil@2000'
    )
    print("Database Connected")
except Exception as e:
    print("Error: ",e)
    print("Database Connection Failed")

connection.autocommit = True # "autocommit" set to True, so you don't have to commit your queries.
cursor = connection.cursor()

# Middleware
def checkSession():

    try:
        email = s['email']
        return True
    except Exception as e:
        print("Error: ",e)
        return False


# Create your views here.

def home(request):
    return HttpResponse('<h1> Welcome to meme application ! </h1>')

def register(request):

    sessionExists = checkSession()
    if sessionExists == False:

        if request.method == 'POST':

            #collect all data from client
            name = request.POST['name']
            contact = request.POST['contact']
            email = request.POST['email']
            password = request.POST['password']

            # print
            print(f'name: {name}')
            print(f'contact: {contact}')
            print(f'Email: {email}')
            print(f'Password: {password}')

            password = password.encode()

            # Hash our password
            hashed = bcrypt.hashpw(password,bcrypt.gensalt())

            hashed = hashed.decode('utf-8')

            # create user dictionary
            userData = {
                'name' : name,
                'contact' : contact,
                'email' : email,
                'password' : hashed
            }

            # register user
            response = registerUser(userData,cursor)

            # print user data
            print('Response: ')
            print(response)

            if response['statusCode'] == 200:
                # Session store
                s['email'] = userData['email']
                s['password'] = userData['password']

                print("Session: ")
                print(s)

                # return render(request, 'register.html',{'message': 'Successfully received'})
                return redirect('/memes/')
            else:
                return render(request, 'register.html',{'message': 'Already registered'})
               
        else:  # elif request.method=="GET"
            return render(request,'register.html')
        
    else:
        return redirect('/memes/')

    
def login(request):

    sessionExists = checkSession()

    if sessionExists == False:

        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            #print
            print('Email: ')
            print(email)

            print('Password: ')
            print(password)

            # create user dict

            userData = {
                'email' : email,
                'password' : password
            }

            response = loginUser(userData,cursor)
            if response['statusCode'] == 200:
                # Session store
                s['email'] = userData['email']
                s['password'] = userData['password']

                print("Session: ")
                print(s)

                # return render(request, 'login.html',{'message': 'Successfully Logged In'})
                return redirect('/memes/')
            elif response['statusCode'] == 503 and response['message'] == 'passworderror':
                return render(request, 'login.html',{'message': 'Password Not Matched'})
            else:
                return render(request, 'login.html',{'message': 'Not Registered'})

        else:
            return render(request,'login.html')
    
    else:
        return redirect('/memes/')
    
def logout(request):
    try:
        s.clear()
        return redirect('/login/')
    except:
        return redirect('/memes/')
    
def getmemes(request):
    sessionExists = checkSession()

    # https://api.imgflip.com/get_memes

    r = requests.get('https://api.imgflip.com/get_memes') 

    meme_data = r.json()

    if sessionExists == False:
        return redirect('/login/')
    else:

        # [{}, {},{}]
        # Meme Name
        # Meme URL
        # Meme ID

        print(meme_data['data']['memes'])

        context = {
            'memes_metadata' : r.json()['data']['memes']
        }

        return render(request,'memes.html',context=context)
    
def editmeme(request):

    sessionStatus = checkSession()
    
    if sessionStatus:
        # Display edit page
        template_id = request.GET['id']

        context = {
            'meme_id' : template_id
        }

        return render(request, 'editmeme.html', context=context)
    else:
        return redirect('/login/')
    
def memedetails(request):
    sessionStatus = checkSession()
    
    if sessionStatus:
        if request.method == 'POST':
            template_id = request.POST['id']
            text0 = request.POST['text0']
            text1 = request.POST['text1']

            # POST request Meme API
            payload = {
                'template_id' : template_id,
                'username' : 'Nikhil_kumar',
                'password' : 'Nikhil@2000',
                'text0' : text0,
                'text1' : text1
            }

            response = requests.request('POST', 'https://api.imgflip.com/caption_image', params = payload).json()

            print('response: ')
            print(response)

            html_str = f'''
                           <h1>Response</h1>
                           <img style="height: 300px; width: 300px" src="{response['data']['url']}" alt "meme">
                           <a href="{response['data']['url']}">View Image</a> 
                        '''
            return HttpResponse(html_str)
    else:
        return redirect('/login/')