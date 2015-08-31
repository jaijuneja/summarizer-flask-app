from __future__ import division
import networkx
from pytldr.nlp import Tokenizer
from pytldr.summarize import RelevanceSummarizer


def rank_news(news_titles, length=5, weighting='frequency', norm=None):

    tokenizer = Tokenizer()

    news_titles = [tokenizer.sanitize_text(title) for title in news_titles]

    return_articles = length if length > 1 else round(len(news_titles) * length)
    return_articles = int(return_articles)

    # Compute the word frequency matrix. If norm is set to 'l1' or 'l2' then words are normalized
    # by the length of their associated sentences (such that each vector of sentence terms sums to 1).
    word_matrix = RelevanceSummarizer._compute_matrix(news_titles, weighting=weighting, norm=norm)

    # Build the similarity graph by calculating the number of overlapping words between all
    # combinations of sentences.
    similarity_matrix = (word_matrix * word_matrix.T)

    similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)
    scores = networkx.pagerank(similarity_graph)

    ranked_articles = sorted(
        ((score, ndx) for ndx, score in scores.items()), reverse=True
    )

    top_articles = [ranked_articles[i][1] for i in range(return_articles)]
    top_articles.sort()

    return top_articles