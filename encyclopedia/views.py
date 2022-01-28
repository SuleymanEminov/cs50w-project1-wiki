from cProfile import label
from lib2to3.pytree import convert
from logging import PlaceHolder
from django.shortcuts import redirect, render

from . import util

from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown


class SearchForm(forms.Form):
    """Class for Search form"""
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Encyclopedia"
    }))

class CreateForm(forms.Form):
    """
    Create form. Contains CharField for getting title of the entry
    and TextArea for the content of the entry
    """
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={
        "Placeholder": "Page Title",
        "class": "form-control",
        "id": "exampleFormControlTextarea1",
        "rows":"15",

    }))
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={
        "Placeholder": "Enter page's content here",
        "class": "form-control",
        "id": "exampleFormControlTextarea1"
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


def create(request):
    """
    This function allows users to create a new entry
    """

    if request.method == "POST":
        form = CreateForm(request.POST)


        # check if title already exsists
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return redirect(reverse("entry", args=[title]))

            else:
                print("error! Page already exsists")

    return render(request, "encyclopedia/create.html", {
        "search_form": SearchForm(),
        "create_form": CreateForm(),

    })











def convert_md(title): 
    """
    This function converts Md file to HTML and and returns HTML text
    """

    markdowner = Markdown() # This is to convert Markdown to HTML

    converted_data = markdowner.convert(title)

    return converted_data
