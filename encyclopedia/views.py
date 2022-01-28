from lib2to3.pytree import convert
from django.shortcuts import redirect, render

from . import util

from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown


class SearchForm(forms.Form):
    """Class for Search form"""
    title = forms.CharField(widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Encyclopedia"
    }))


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })



def entry(request, title):
    """
    This is a getter function that gets user input from index.html forms,
    and returns back a converted entry if it exsists in the entries directory
    """

    entry_file = util.get_entry(title)

    if entry_file is not None: # entry exsists in the directory
        
        
 
            
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": convert_md(entry_file),
            "search_form": SearchForm()
    })
    else: # entry doesn't exsist
        return render(request, "encyclopedia/404.html", {
            "title": title,
            "search_form": SearchForm()
        })


def search(request):
    """
    This function is a search function that listens to the search form 
    and returns searched article if exsists in the 'entries' directory
    """


    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            entry_file = util.get_entry(title)


            if entry_file:
                # If entry exsists in the entries directory,
                # redirect to that article 
                return redirect(reverse("entry",args=[title]))
            else: #page doesn't exsist, call search page

                related_entries = []

                
                # find articles that have a substring of title and append to 
                # list of related_entries. 
                for entry in util.list_entries():
                    if convert_md(util.get_entry(entry).lower()).find(title.lower()) != -1:
                        related_entries.append(entry)


                print(related_entries)

                
                    
                return render(request, "encyclopedia/search.html", {
                "title": title,
                "related_entries": related_entries,
                "search_form": SearchForm()
            })

    else:
        return redirect(reverse('index'))



def convert_md(title): 
    markdowner = Markdown() # This is to convert Markdown to HTML

    converted_data = markdowner.convert(title)

    return converted_data
