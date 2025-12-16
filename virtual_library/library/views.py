from django.shortcuts import render, get_object_or_404
from .models import Book
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
import os
from .forms import UserRegistrationForm
import asyncio
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.http import JsonResponse
from asgiref.sync import sync_to_async


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Path to your login template
    authentication_form = CustomAuthenticationForm

# Initialize Google Generative AI client
# client = Client(api_key="AIzaSyDfbRDjStUbXZlqiS7mk-bqGLFC1PC3kvo")
genai.configure(api_key="AIzaSyDfbRDjStUbXZlqiS7mk-bqGLFC1PC3kvo")
# model = client.get_model(model="gemini-1.5-pro")
model = genai.GenerativeModel('gemini-1.5-pro')


# User registration view
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'library/register.html', {'form': form})

# User login view
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})

# User logout view
def logout_user(request):
    logout(request)
    return redirect('book_list')

# User profile view (optional)
@login_required
def profile(request):
    return render(request, 'library/profile.html', {'user': request.user})

def home(request):
    # Define the categories for the UI
    categories = [
        {"name": "Fiction", "description": "Explore fictional books", "gradient": "from-blue-500 to-purple-500"},
        {"name": "Science", "description": "Discover scientific reads", "gradient": "from-green-500 to-blue-500"},
        {"name": "History", "description": "Dive into history", "gradient": "from-orange-500 to-red-500"},
        {"name": "Fantasy", "description": "Escape into fantastical worlds", "gradient": "from-purple-500 to-pink-500"},
        {"name": "Thriller", "description": "Thrilling adventures await", "gradient": "from-red-500 to-yellow-500"},
        {"name": "Glamour", "description": "Fall in love with beautiful stories", "gradient": "from-pink-500 to-red-500"},
    ]
    
    # Query all books from the database
    books = Book.objects.all()
    
    # Pass data to the template
    context = {
        "categories": categories,
        "books": books,
    }
    return render(request, "home.html", context)


# Book list view
def book_list(request):
    categories = [
        {"name": "Fiction", "description": "Explore fictional books", "gradient": "from-blue-500 to-purple-500"},
        {"name": "Science", "description": "Discover scientific reads", "gradient": "from-green-500 to-blue-500"},
        {"name": "History", "description": "Dive into history", "gradient": "from-orange-500 to-red-500"},
        {"name": "Fantasy", "description": "Escape into fantastical worlds", "gradient": "from-purple-500 to-pink-500"},
        {"name": "Thriller", "description": "Thrilling adventures await", "gradient": "from-red-500 to-yellow-500"},
        {"name": "Glamour", "description": "Fall in love with beautiful stories", "gradient": "from-pink-500 to-red-500"},
    ]
    
    query = request.GET.get('q', '')
    books = Book.objects.filter(name__icontains=query) if query else Book.objects.all()
    
    context = {
        "categories": categories,
        "books": books,
        "query": query,
    }

    if query:
        books = books.filter(name__icontains=query)  # Modify this query as per your needs

    return render(request, "library/book_list.html", context)


#about us
def about_us(request):
    return render(request, 'library/aboutus.html') 


def book_list_by_category(request, category):
    categories = [
        {"name": "Fiction", "description": "Explore fictional books", "gradient": "from-blue-500 to-purple-500"},
        {"name": "Science", "description": "Discover scientific reads", "gradient": "from-green-500 to-blue-500"},
        {"name": "History", "description": "Dive into history", "gradient": "from-orange-500 to-red-500"},
        {"name": "Fantasy", "description": "Escape into fantastical worlds", "gradient": "from-purple-500 to-pink-500"},
        {"name": "Thriller", "description": "Thrilling adventures await", "gradient": "from-red-500 to-yellow-500"},
        {"name": "Glamour", "description": "Fall in love with beautiful stories", "gradient": "from-pink-500 to-red-500"},
    ]
    
    books = Book.objects.filter(category=category)
    context = {
        "categories": categories,
        "books": books,
        "category_name": category,  # Use category_name here for consistency
    }
    return render(request, "library/book_list_by_category.html", context)


# Book detail view
# Book detail view
def book_detail(request, pk, category=None, category_name=None):
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book}

    # If either category or category_name is provided, include it in the context
    if category or category_name:
        context['category'] = category or category_name

    return render(request, 'library/book_detail.html', context)


@sync_to_async
def chatbot_response(user_message):
    # Replace this logic with your chatbot processing logic.
    if "book" in user_message.lower():
        return "Here are some popular books to explore!"
    return "I can help you with library inquiries. Please ask a specific question."

async def chatbot_view(request):
    if request.method == "POST":
        import json
        body = json.loads(request.body)
        user_message = body.get('message', '')
        response = await chatbot_response(user_message)
        return JsonResponse({"response": response})
    return JsonResponse({"error": "Invalid request method"}, status=400)


# Async chatbot API view
@csrf_exempt
async def chatbot(request):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)
            user_query = data.get('query', '')

            # Fetch books asynchronously
            books = await sync_to_async(lambda: list(Book.objects.values_list('name', flat=True)))()
            books_list = ', '.join(books)

            # Format the prompt
            # prompt_template = f"These are my Books I have stored in my store Based on available books: {books_list}, answer the following specified book summary and if below book {user_query} if these not listed show me not available book. User_Question : {user_query}"

            prompt_template = f" These are my books: {books_list} can you check these book {user_query} is available in above list (Yes / No)? and give me summary of these book {user_query}"

            # Call model.generate_content in a thread-safe way
            response = await asyncio.to_thread(model.generate_content, prompt_template)

            return JsonResponse({"response": response.text}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


