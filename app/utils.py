import logging
import re
from typing import Optional, List, Dict

import requests
from datetime import datetime

from app.models import UrlList
from config import config

logger = logging.getLogger(' UTILS ')
logger.setLevel(level=config.LOGGING_LEVEL)

community_id = -278573

get_posts_url = "https://api.vk.com/method/wall.search?" \
                f"owner_id={community_id}" \
                "&domain=hse_career" \
                "&query=%23вакансиидня" \
                "&owners_only=0" \
                f"&count={config.POSTS_COUNT}" \
                f"&access_token={config.VK_TOKEN}" \
                "&v=5.131"


def new_post_available(posts: List[Dict]):
    logger.info("Checking for new posts")
    last_post_id = posts[0].get("id")

    if config.LAST_POST_ID is None:
        config.LAST_POST_ID = last_post_id
        return False

    if config.LAST_POST_ID == last_post_id:
        return False
    else:
        config.LAST_POST_ID = last_post_id
        return True


def get_post_urls(post_index: int = 0) -> UrlList:
    result = requests.get(get_posts_url).json()
    posts = result.get("response").get("items")

    if not new_post_available(posts):
        logger.info("No new posts found")
        return UrlList(
            teletype=[],
            careerspace=[],
            hh=[],
            other=[]
        )

    newest_post = posts[post_index].get("text")
    pre_list = re.findall("(?P<url>https?://[^\s]+)", newest_post)

    teletype_list, careerspace_list, hh_list, other_list = [], [], [], []

    if datetime.now().weekday() < 5:
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
