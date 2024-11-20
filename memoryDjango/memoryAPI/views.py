from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# AVOID HARDCODING URLS. DIRECT TO LIST OF URLS AND CATCH THE NAME.

class NewMemoryForm(forms.Form):
    memory = forms.CharField(label="New memory")

# Create your views here.
def index(request):
    return render(request, "memoryAPI/index.html")

def memory(request):
    if "mems" not in request.session:
        request.session["mems"] = []

    if request.method == "POST":
        form = NewMemoryForm(request.POST)
        if form.is_valid():
            mem = form.cleaned_data["memory"]
            request.session["mems"] += [mem] 
            return HttpResponseRedirect(reverse("memoryAPI:index"))
        else:
            return render(request, "memoryAPI/memory.html", {
                "form": form
            })

    return render(request, "memoryAPI/memory.html", {
        "mems":request.session["mems"],
        "memory": NewMemoryForm()
        })

def greet(request, name):

    if len(name) > 5:
        processed_name = "Too long name bruh"
    else:
        processed_name = name.capitalize()

    return render(request, "memoryAPI/greet.html", {
        "name": processed_name
    })