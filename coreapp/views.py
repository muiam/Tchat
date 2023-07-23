from django.shortcuts import render
import requests
import aiohttp
import asyncio
from django.http import JsonResponse, HttpResponse

# Create your views here.


# In-memory cache to store user data
user_cache = {}

async def fetch_user(session, user_id):
    user_url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    async with session.get(user_url) as response:
        if response.status == 200:
            user_data = await response.json()
            # Store user data in the cache
            user_cache[user_id] = user_data

async def fetch_posts():
    url = 'https://jsonplaceholder.typicode.com/posts'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                posts = await response.json()

                # Fetch user details asynchronously for each post
                tasks = [fetch_user(session, post['userId']) for post in posts]
                await asyncio.gather(*tasks)

                # Add user details to the post dictionary
                for post in posts:
                    post['user'] = user_cache.get(post['userId'])

                return posts

def index(request):
    # Run the asynchronous function within the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    posts = loop.run_until_complete(fetch_posts())
    
    if posts is not None:
        context = {'posts': posts}
        return render(request, 'index.html', context)
    else:
        context = {'error_message': 'Failed to fetch data from the API'}
        return render(request, 'error.html', context)

def login(request):
    if request.method == "POST":
        # # Get the username and password from the POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        users_url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(users_url)
        users_data = response.json()

        # Find a user with matching username and zip code (assuming zip code is used as password)
        authenticated_user = None
        for user in users_data:
            if user['username'] == username and user['address']['zipcode'] == password:
                authenticated_user = user
                break

        if authenticated_user:
            
            return JsonResponse({'user':authenticated_user}, safe=False)
        

        else:
            # Invalid username or zip code
            return JsonResponse({'user':'0'}, safe=False)

    # If the request method is not POST, render the login template
    return render(request, 'index.html')


def post_detail(request, post_id):
    comments_url = f'https://jsonplaceholder.typicode.com/posts/{post_id}/comments'
    response = requests.get(comments_url)
    comments = response.json()
    for comment in comments:
        postid= comment['postId']
        posturl= f'https://jsonplaceholder.typicode.com/posts/{postid}'
        response=requests.get(posturl)
        post=response.json()
    
    num_comments = len(comments)
    
    return render(request, 'post_detail.html', {'comments': comments, 'total':num_comments,'title':post['title'], 'body':post['body']})


async def fetch_posts():
    url = 'https://jsonplaceholder.typicode.com/posts'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                posts = await response.json()
                return posts
            else:
                return None

async def fetch_user(session, user_id):
    user_url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    async with session.get(user_url) as response:
        if response.status == 200:
            user_data = await response.json()
            return user_data
        else:
            return None

async def myposts(request):
    # Fetch all posts asynchronously
    posts = await fetch_posts()

    if posts is not None:
        # Create a set of user IDs for efficient lookup
        user_ids = {post['userId'] for post in posts}

        # Fetch user details asynchronously for each user
        async with aiohttp.ClientSession() as session:
            user_tasks = [fetch_user(session, user_id) for user_id in user_ids]
            user_responses = await asyncio.gather(*user_tasks)

        # Create a dictionary to store user details with user ID as the key
        user_details = {user['id']: user for user in user_responses if user is not None}

        # Filter posts for the user with the username 'Bret'
        filtered_posts = [post for post in posts if user_details.get(post['userId'], {}).get('username') == 'Bret']

        context = {'posts': filtered_posts}
        return render(request, 'myposts.html', context)
    else:
        context = {'error_message': 'Failed to fetch data from the API'}
        return render(request, 'error.html', context)

def feedposts(usernames):
    posts_response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts_data = posts_response.json()

    posts = []
    for post_data in posts_data:
        owner_id = post_data['userId']
        user_response = requests.get(f'https://jsonplaceholder.typicode.com/users/{owner_id}')
        user_data = user_response.json()
        owner_username = user_data['username']

        if owner_username in usernames:
            posts.append({
                'owner_username': owner_username,
                'title': post_data['title'],
                'content':post_data['body'],
                'id': post_data['id']
            })

    return posts

def myfeed(request):
    interested_usernames = ['Antonette', 'Samantha', 'Kamren']
    posts = feedposts(interested_usernames)
    return render(request, 'myfeed.html', {'posts': posts})



def fetch_user_data(username):
    users_response = requests.get('https://jsonplaceholder.typicode.com/users')
    users_data = users_response.json()

    for user_data in users_data:
        if user_data['username'] == username:
            return user_data

    return None
def profile(request):
    profile_data = fetch_user_data('Bret')  # Fetch data for the username 'Bret'

    return render(request, 'profile.html', {'profile_data': profile_data})