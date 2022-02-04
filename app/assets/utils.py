import re
import requests

from app.assets.modeller import UrlList
from config import config

request_url = "https://api.vk.com/method/wall.search?" \
              "owner_id=-278573" \
              "&domain=hse_career" \
              "&query=%23вакансиидня" \
              "&owners_only=0" \
              "&count=10" \
              f"&access_token={config.VK_TOKEN}" \
              "&v=5.131"


def get_post_urls(post_index: int = 0) -> UrlList:
    result: dict = requests.get(request_url).json()
    newest_post = result.get("response").get("items")[post_index].get("text")
    pre_list = re.findall("(?P<url>https?://[^\s]+)", newest_post)
    return UrlList(
        teletype=[url for url in pre_list if 'teletype' in url],
        careerspace=[url for url in pre_list if 'careerspace' in url],
        hh=[url for url in pre_list if 'hh' in url],
        other=None
    )
