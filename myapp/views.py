from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
# Create your views here.
def home(request):
  return render(request,'base.html')


BASE_URL = 'https://losangeles.craigslist.org/search?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
def new_search(request):
  search = request.POST.get('search')    #request.POST returns dictionary and get returns specific one and only
  models.Search.objects.create(search=search)
  final_url = BASE_URL.format(quote_plus(search))
  response = requests.get(final_url)
  data = response.text
  soup = BeautifulSoup(data,features='html.parser')


  final_postings = []
  post_listings = soup.find_all('li',class_='result-row')
  for post in post_listings:
    post_title = post.find(class_='result-title').text
    post_url = post.find('a').get('href')
    if post.find(class_='result-price'):
     post_price = post.find(class_='result-price').text
    else:
      post_price = 'N/A' 

    if post.find(class_='result-image').get('data-ids'):
      post_img = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
      post_img = BASE_IMAGE_URL.format(post_img)
      print(post_img)
    else:
      post_img = 'https://craigslist.org/images/peace.jpg'  

    final_postings.append((post_title,post_url,post_price,post_img))




  # print(data)
  context = {
    'search':search,
    'final_postings':final_postings,
  }
  return render(request,'myapp/new_search.html',context)  