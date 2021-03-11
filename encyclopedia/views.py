from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from . import util
import random
import re

class NewCreateEntryForm(forms.Form):
    create_title = forms.CharField(label="Title", max_length=30, error_messages={'Duplicate': 'Encyclopedia entry already exists'})
    create_body = forms.CharField(widget=forms.Textarea, label="Body")

class NewEditEntryForm(forms.Form):
    create_body = forms.CharField(widget=forms.Textarea, label="Body")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    try:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdowner.convert(util.get_entry(title))
        })
    except:
        return render(request, "encyclopedia/results.html", {
            "error_message": "No results found"
        })

def search(request):
    input = request.GET['q'].lower()
    list_titles = util.list_entries()
    list_result = []
    for list_title in list_titles:
        list_result.append(list_title.lower())
    if input in list_result:
        return HttpResponseRedirect(reverse("wiki:title", args=(input,)))
    elif any(input):
        partials = []
        for title in list_result:
            if input in title:
                partials.append(title.capitalize())
        if len(partials) > 0:
            return render(request, "encyclopedia/results.html", {
                "results": partials
            })
        else:
            return render(request, "encyclopedia/results.html", {
            "error_message": "No results found"
        })
    else:
        return render(request, "encyclopedia/results.html", {
            "error_message": "No results found"
        })

def create(request):
    if request.method == "POST":
        entryInput = NewCreateEntryForm(request.POST)
        if entryInput.is_valid():
            entryTitle = (entryInput.cleaned_data["create_title"])
            list = util.list_entries()
            if entryTitle in list:
                return render(request, "encyclopedia/create.html", {
                "create_form": entryInput,
                "error_message": "Sorry, title is already taken"
                })
            else:
                entryBody = (entryInput.cleaned_data["create_body"])
                util.save_entry(entryTitle, entryBody)
                return HttpResponseRedirect(reverse("wiki:title", args=(entryTitle,)))
        else:
            return render(request, "encyclopedia/create.html", {
            "create_form": entryInput,
            "error_message": "Sorry, the form was not valid"
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "create_form": NewCreateEntryForm()
        })

def edit(request, title):
    if request.method == "POST":
        entryInput = NewEditEntryForm(request.POST)
        if entryInput.is_valid():
            entryBody = (entryInput.cleaned_data["create_body"])
            util.save_entry(title, entryBody)
            return HttpResponseRedirect(reverse("wiki:title", args=(title,)))
        else:
            return render(request, "encyclopedia/create.html", {
                "edit_form": entryInput,
                "error_message": "Sorry, the form was not valid"
            })
    else:
        initial_dict = {"create_body": util.get_entry(title)}
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": NewEditEntryForm(None, initial = initial_dict)
        })

def random_page(request):
    list_titles = util.list_entries()
    random_result = random.choice(list_titles)
    return HttpResponseRedirect(reverse("wiki:title", args=[random_result]))