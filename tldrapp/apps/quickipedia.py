import wikipedia as wiki
import summarizer
from .. import config
from requests import ConnectionError


def search(query):
    try:
        results = wiki.search(query)
        results = [(r, r.replace(' ', config.QUICKIPEDIA_SPACE_PLACEHOLDER)) for r in results]
        return results, None
    except ConnectionError:
        error = 'Could not connect to Wikipedia.'
        return [], error


def url_to_summary(extension, algorithm):
    page_id = extension.replace(config.QUICKIPEDIA_SPACE_PLACEHOLDER, ' ')
    page = wiki.page(page_id)
    title = page.title
    return title, summarizer.summarize(page.content, algorithm, 0.2)