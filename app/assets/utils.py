import re
import requests

from app.assets.modeller import UrlList
from config import config

request_url = "https://api.vk.com/method/wall.search?" \
              "owner_id=-278573" \
              "&domain=hse_career" \
              "&query=%23вакансиидня" \
              "&owners_only=0" \
              f"&count={config.POSTS_COUNT}" \
              f"&access_token={config.VK_TOKEN}" \
              "&v=5.131"


def get_post_urls(post_index: int = 0) -> UrlList:
    result = requests.get(request_url).json()

    newest_post = result.get("response").get("items")[post_index].get("text")
    pre_list = re.findall("(?P<url>https?://[^\s]+)", newest_post)

    teletype_list, careerspace_list, hh_list, other_list = [], [], [], []

    for url in pre_list:
        if 'teletype' in url:
            teletype_list.append(url)
        elif 'careerspace' in url:
            careerspace_list.append(url)
        elif 'hh' in url:
            hh_list.append(url)
        else:
            other_list.append(url)

    return UrlList(
        teletype=teletype_list,
        careerspace=careerspace_list,
        hh=hh_list,
        other=other_list
    )
