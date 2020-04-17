from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
import pyrebase

config = {
    "apiKey": "AIzaSyDc7jiAq7NPnPTq69r2eacfxotV8bCezOk",
    "authDomain": "tagalog-corpus.firebaseapp.com",
    "databaseURL": "https://tagalog-corpus.firebaseio.com",
    "projectId": "tagalog-corpus",
    "storageBucket": "tagalog-corpus.appspot.com",
    "messagingSenderId": "392692588813",
    "appId": "1:392692588813:web:d36bd376509ecd81c81044",
    "measurementId": "G-X5T228PQ03"
}
firebase = pyrebase.initialize_app(config)

fireAuth = firebase.auth()
database = firebase.database()

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name': 'Jake'})

def signIn(request):
    return render(request, 'signin.html')

def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = fireAuth.sign_in_with_email_and_password(email,password)
    except:
        message='invalid credentials'
        return render(request, 'signin.html', {"message":message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, 'welcome.html', {"email": email})

def logout(request):
    try:
        del request.session['uid']
    except KeyError:
            pass
    return render(request, 'signin.html')

def signUp(request):
    return render(request, 'signup.html')

def postsignup(request):

    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = fireAuth.create_user_with_email_and_password(email, password)
    except:
        message = 'unable to create account.  try again'
        return render(request, 'signin.html', {"message": message})
    uid = user['localId']
    print(user)
    data = {'name': name, 'status': '1'}

    database.child('users').child(uid).child('details').set(data)

    return render(request, 'signin.html')

def create(request):
    return render(request, 'create.html')

def postcreate(request):

    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)

    millis = int(time.mktime(time_now.timetuple()))
    work = request.POST.get('work')
    progress = request.POST.get('progress')

    try:
        tokenId = request.session['uid']

        a = fireAuth.get_account_info(tokenId)
        a = a['users'][0]['localId']

        data = {
            'work': work,
            'progress': progress
        }

        database.child('users').child(a).child('reports').child(millis).set(data, tokenId)
        name = database.child('users').child(a).child('details').child('name').get(tokenId).val()

        return render(request, 'welcome.html', {'email': name})
    except KeyError:
        message = 'Oops!  User Logged Out.  Please sign in again.'
        return render(request, 'signin.html', {"message": message})

def check(request):
    tokenId = request.session['uid']

    a = fireAuth.get_account_info(tokenId)
    a = a['users'][0]['localId']

    timestamps = database.child('users').child(a).child('reports').shallow().get(tokenId).val()
    list_time = []
    for timestamp in timestamps:
        list_time.append(timestamp)
    list_time.sort(reverse=True)
    print(list_time)
    work = []
    for item in list_time:

        wor = database.child('users').child(a).child('reports').child(item).get('work').val()
        work.append(wor)
    print(work)
    return render(request, 'check.html')

def search_word(request):

    word = request.POST['word']
    pos = database.child('words_and_tags').child(word).get().val()
    tagset = {}
    with open("resources/tagset.txt", mode="r", encoding="utf-8") as infile:
        lines = infile.readlines()
        for line in lines:
            tagset[line.split('--')[1].lower()] = line.split('--')[0]
    data = {
        'tag': pos,
        'tag_normalized': tagset[pos],
        'word': word,
    }
    print(data)
    has_n = ''
    if tagset[pos][0] in 'aeiou':
        has_n = 'n'

    return render(request, 'result.html', {
        'tag': pos[0:-2].upper(),
        'tag_normalized': tagset[pos],
        'word': word,
        'has_n': has_n
    })

def pop_database(request):
    import re
    with open("resources/all_words.txt", mode="r", encoding="ANSI") as infile:
        lines = infile.readlines()
        print(len(lines))
        tagged_dict = {}
        for line in lines:
            line = line.lower()
            if re.match('[^a-zA-Z]', line):
                continue
            else:
                if len(line.split('\t')) == 2:
                    tagged_dict[line.split('\t')[0]] = line.split('\t')[1]
        for key,value in tagged_dict.items():
            try:
                database.child('words_and_tags').child(key).set(value)
            except:
                print(line[0], ': has an error')
