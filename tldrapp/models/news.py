from flask.ext.sqlalchemy import SQLAlchemy

# Will need to subclass the Summary model to include things like
# image, news source, original published date etc.
# Need to write a newsbot web crawler to populate tables with latest news
# from a selection of websites (BBC, Fox, CNN, Al Jazeera etc.)
# Crawler should be a cookie cutter, so that any given website can be
# crawled at a later date, perhaps even one provided by the user