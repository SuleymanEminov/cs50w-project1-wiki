from django.shortcuts import render

from . import util

from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    """
    This is a getter function that gets user input from index.html forms,
    and returns back a converted entry if it exsists in the entries directory
    """

    if request.method == "POST":

        entry_title = request.POST['q']


    if (util.get_entry(entry_title) is not None):
        markdowner = Markdown() # This is to convert Markdown to HTML

        entry = util.get_entry(entry_title) # get 

        converted_data = markdowner.convert(entry) 
        
        return render(request, "encyclopedia/display.html", {
        "title": entry_title,
        "entry": converted_data,
    })
    else:
        return render(request, "encyclopedia/404.html", {
            "title": entry_title
        })

