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

def search_word(request):

    word = request.POST['word']
    pos = database.child('words_and_tags').child(word).get().val()
    tagset = {}
    with open("resources/tagset.txt", mode="r", encoding="utf-8") as infile:
        lines = infile.readlines()
        for line in lines:
            tagset[line.split('--')[1].lower()] = line.split('--')[0]

    if pos == None:
        return render(request, 'failed_result.html', {
            'err': TypeError,
            'word': word,
        })

    data = {
        'tag': pos,
        'tag_normalized': tagset[pos],
        'word': word,
    }

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
