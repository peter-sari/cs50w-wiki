from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random
from . import util
from django.core.files.base import ContentFile

markdowner = Markdown()

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(widget=forms.Textarea(), label="Bodycopy")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def nosuchentry(request):
    return render(request, "encyclopedia/nosuchentry.html")

def exists(request):
    return render(request, "encyclopedia/exists.html")

def searching(request):
    if request.method == "POST":
        title = request.POST.__getitem__("title")
        entrieslist = util.list_entries()

        for entry in entrieslist:
            if title.lower() == entry.lower():
                return HttpResponseRedirect(f"/wiki/{entry}")
        
        resultlist = []
        for entry in entrieslist:
            if title.lower() in entry.lower():
                resultlist.append(entry)
        
        if len(resultlist) == 0:
            return render(request, "encyclopedia/nosuchentry.html")
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": resultlist
            })



def entry(request, title):
    entries = util.list_entries()
    for entry in entries:
        if title.lower() == entry.lower():
            return render(request, f"encyclopedia/entry.html", {
                "entryname": entry,
                "content": markdowner.convert(util.get_entry(title))
            })
    return HttpResponseRedirect("/nosuchentry")

def randomed(request):
    myrandom = random.choice(util.list_entries())
    return  HttpResponseRedirect(f"wiki/{myrandom}")

def create(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
        
        if util.search(util.list_entries(), title):
            return HttpResponseRedirect(reverse("encyclopedia:exists"))

        else:
            with open(f'entries\\{title}.md', 'w+') as NewEntry:
                NewEntry.write(body)
            return HttpResponseRedirect("wiki/{title}".format(title=title))
        
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewTaskForm()
        })

def entryname(request, entryname):

        with open(f'entries\\{entryname}.md', 'r') as ExistingEntry:
            existing = ExistingEntry.read                

            class NewEntryForm(forms.Form):
                title = forms.CharField(label="Title", initial=entryname) 
                body = forms.CharField(label="Bodycopy", initial=existing, widget=forms.Textarea() )
            
            return render(request, "encyclopedia/edit.html", {
                "form": NewEntryForm()
            })
        
def edit(request):
        if request.method == "POST":
            form = NewTaskForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                body = form.cleaned_data["body"]
            with open(f'entries\\{title}.md', 'w+') as NewEntry:
                NewEntry.write(body)
            return HttpResponseRedirect("wiki/{title}".format(title=title))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": NewTaskForm()
            })