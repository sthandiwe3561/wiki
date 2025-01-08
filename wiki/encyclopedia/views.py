from django.shortcuts import render,redirect
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry_page(request,title):
    #fecthing the content of the entry
    content = util.get_entry(title)

    return render(request,"encyclopedia/entry_page.html", {
        "content":content , "title": title.capitalize()
    })

def search(request):
    if request.method == "POST":
        value = request.POST.get("q", "")
        if value:
            content = util.get_entry(value)

            if content:
               return render("encyclopedia/entry_page",{
                "content":content
               })
            else:
              lower_value = value.lower()
              entries = util.list_entries()
              partial_matches = [entry for entry in entries if lower_value in entry.lower()]
              return render(request,"encyclopedia/search_page.html", {
                  "results": partial_matches, "query":value
              })

       
    else:
        return redirect(reverse("index"))

