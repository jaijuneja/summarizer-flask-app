import wikipedia as wiki
import summarizer
from .. import config


def search(query):
    results = wiki.search(query)
    results = [(r, r.replace(' ', config.QUICKIPEDIA_SPACE_PLACEHOLDER)) for r in results]
    return results


def url_to_summary(extension, algorithm):
    page_id = extension.replace(config.QUICKIPEDIA_SPACE_PLACEHOLDER, ' ')
    page = wiki.page(page_id)
    title = page.title
    return title, summarizer.summarize(page.content, algorithm, 0.2)