import requests
from app.utils import new_post_available, get_post_urls, get_posts_url

result = requests.get(get_posts_url).json()
posts = result.get("response").get("items")
