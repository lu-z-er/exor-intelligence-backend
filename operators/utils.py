from newsplease import NewsPlease
from operators.exor_errors import FetchArticleError
import json 

def taskmaster(url, cla_callable, insert_callable):
    scrape = NewsPlease.from_url(url)
    try:
        if scrape:
            opse = scrape.get_serializable_dict()
            result = cla_callable(opse["description"])
            exor_format = {
                    'authors': opse['authors'],
                    'date_download': opse["date_download"],
                    "updatedAt": None,
                    "publishedAt": opse["date_publish"],
                    'summary': opse["description"],
                    'filename': opse["filename"],
                    "imageUrl": opse["image_url"],
                    'language': opse["language"],
                    'description': opse["maintext"],
                    'source': opse["source_domain"],
                    'title': opse["title"],
                    'url': opse["url"],
                    "isFakeNews": False,
                    "category": result['labels'][0],
                    "isUserSubmitted": True
                }
            return exor_format
        else:
            raise FetchArticleError("Unable to fetch the Article!!")
    except Exception:
        raise