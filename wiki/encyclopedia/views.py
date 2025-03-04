import random
from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry (request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            'message': "The requested page was not found."
        })
    
    marked_content = markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": marked_content
    })

def edit_entry(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            'message': "The requested page was not found."
        })
    
    if request.method == 'POST':
        # Get the updated content from the form
        updated_content = request.POST.get("content")

        # Save the updated entry
        util.save_entry(title, updated_content)

        # Redirect to the entry page after saving
        return redirect('entry', title=title)
    
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "content": content
    })

def search(request):
    query = request.GET.get('q', '') # Getting the Search Query

    if query:
        entries = util.list_entries() # Get all Entries
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]

        # Cheking if there is a match
        if query.lower() in [entry.lower() for entry in entries]:
            return entry(request, query)
        
        # Otherwise render a search page

        return render(request, "encyclopedia/search.html", {
            'query': query,
            'entries': matching_entries
        })
    
    return render(request, "encyclopedia/search.html", {
        'query': query,
        'entries': []
    })

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        # Check if the entry already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
        
        # Save the new entry
        util.save_entry(title, content)

        #Redirect to the new entry page
        return redirect('entry', title=title)
    
    # If GET request, just render the form
    return render(request, "encyclopedia/create.html")

def random_page(request):
    # Get a list of all entries
    entries = util.list_entries()
    
    # Choose a random entry from the list
    random_entry = random.choice(entries)
    
    # Redirect the user to the corresponding wiki page (e.g., /wiki/css)
    return redirect('entry', title=random_entry)