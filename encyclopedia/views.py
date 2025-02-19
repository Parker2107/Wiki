from django.shortcuts import render, redirect
from django.http import HttpResponse
from markdown2 import Markdown
from . import util
import os
import random

md = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load(request, name):
    con = util.get_entry(name)
    if con is None:
        return render(request, "encyclopedia/error404.html")

    content_html = md.convert(con)
    return render(request, "encyclopedia/load.html", {
        "name": name,
        "content": content_html,
    })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query in entry.lower()]  # Case-insensitive partial match

    if len(matching_entries) == 1:
        return load(request,matching_entries[0])

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": matching_entries,
    })

def new(request):
    return render(request, "encyclopedia/newpage.html")

def renderpage(request):
    if request.method == "POST":
        heading = request.POST.get("heading", "").strip()
        body = request.POST.get("body", "").strip()

        if not heading or not body:
            return render(request, "encyclopedia/error404.html")

        l1 = heading.split()
        if len(l1) < 2:
            return render(request, "encyclopedia/error404.html")

        name = l1[1]
        entries = util.list_entries()
        if name in entries:
            return render(request, "encyclopedia/error404.html")
        s_name = "".join(c for c in name if c.isalnum())
        s_name = s_name+".md"
        fname = os.path.join("entries", s_name)

        try:
            with open(fname, "w") as file:
                file.write(f"{heading}\n{body}")
        except IOError:
            return render(request, "encyclopedia/error404.html")

        return redirect("load", name=name)

    return render(request, "encyclopedia/error404.html")

def randompage(request):
    l1 = util.list_entries()
    n = len(l1)
    x = random.randint(0,n-1)
    return redirect(f"/wiki/{l1[x]}")

def edit(request, name):
    body = util.get_entry(name)
    return render(request, "encyclopedia/editform.html", {
        "name": name,
        "body": body,
    })

def editpage(request,name):
    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if not body:
            return render(request, "encyclopedia/error404.html")
        fname="entries/"+name+".md"
        try:
            with open(fname, "w") as file:
                file.write(f"{body}")
        except IOError:
            return render(request, "encyclopedia/error404.html")

        return redirect("load", name=name)

    return render(request, "encyclopedia/error404.html")
