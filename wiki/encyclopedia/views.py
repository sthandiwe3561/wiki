from django.urls import reverse
from django.shortcuts import render,redirect
from . import util
from django.contrib import messages
from markdown2 import Markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry_page(request,title):
    #fecthing the content of the entry
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Page '{title}' not found."
        })
    
    markdowner = Markdown()
    content = markdowner.convert(content)

    return render(request,"encyclopedia/entry_page.html", {
        "content":content , "title": title.capitalize()
    })

def search(request):
    if request.method == "POST":
        value = request.POST.get("q", "")
        if value:
            content = util.get_entry(value)

            if content:
               return redirect(reverse("entry_page", args=[value]))
            else:
              lower_value = value.lower()
              entries = util.list_entries()
              partial_matches = [entry for entry in entries if lower_value in entry.lower()]
              return render(request,"encyclopedia/search_results.html", {
                  "results": partial_matches, "query":value
              })
    else:
        return redirect(reverse("index"))

def new_page (request):
    if request.method == "POST":
        title = request.POST.get("title","").strip()
        content = request.POST.get("content","").strip()
        existing_entries = [entry.lower() for entry in util.list_entries()]  # Convert to lowercase for case-insensitive check

        if title.lower() in existing_entries:
                messages.error(request, f"The entry '{title}' already exists.")
                return redirect(reverse("new_page"))
        
        markdown_content = f"# {title}\n\n{content}"

        util.save_entry(title,markdown_content)
        return redirect(reverse("index"))
    else:
        return render(request,"encyclopedia/new_page.html")

def edit_entry(request,title):

    content = util.get_entry(title)  

    if content is None:
        messages.error(request, f"Content for '{title}' not available.")
        return redirect(reverse("index"))
    
    if request.method == "POST":
        updated_content = request.POST.get("content", "").strip()  # Get new content
        util.save_entry(title, updated_content)  #  Save changes
        return redirect(reverse("entry_page", args=[title]))  #Redirect to the updated page

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content  # Pass the existing content to pre-fill the textarea
    })

def random_entry(request):
    """
    Selects a random encyclopedia entry and redirects to its page.
    """
    entries = util.list_entries()  #Get the list of all entries
    if not entries:  #Handle case where there are no entries
        return redirect(reverse("index"))  # Redirect to index if no entries exist

    random_title = random.choice(entries)  #Select a random entry
    return redirect(reverse("entry_page", args=[random_title]))  


        

