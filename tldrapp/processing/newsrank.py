import numpy as np
from pytldr.nlp import Tokenizer
from pytldr.summarize import RelevanceSummarizer


def rank_news(news_titles, binary_matrix=True, length=0.5):
    tokenizer = Tokenizer()
    sentence_rank = RelevanceSummarizer()

    news_titles = [tokenizer.sanitize_text(title) for title in news_titles]

    matrix = sentence_rank._compute_matrix(news_titles, weighting='frequency')

    # Sum occurrences of terms over all sentences to obtain document frequency
    doc_frequency = matrix.sum(axis=0)

    if binary_matrix:
        matrix = (matrix != 0).astype(int)

    top_news = []
    return_articles = length if length > 1 else round(len(news_titles) * length)
    return_articles = int(return_articles)
    for _ in xrange(return_articles):
        # Take the inner product of each sentence vector with the document vector
        article_scores = matrix.dot(doc_frequency.transpose())
        article_scores = np.array(article_scores.T)[0]

        # Grab the top sentence and add it to the summary
        top_article = article_scores.argsort()[-1]
        top_news.append(top_article)

        # Remove all terms that appear in the top sentence from the document
        terms_in_top_sentence = (matrix[top_article, :] != 0).toarray()
        doc_frequency[terms_in_top_sentence] = 0

        # Remove the top sentence from consideration by setting all its elements to zero
        # This does the same as matrix[top_article, :] = 0, but is much faster for sparse matrices
        matrix.data[matrix.indptr[top_article]:matrix.indptr[top_article+1]] = 0
        matrix.eliminate_zeros()

    # Return the location of the top news articles from the input list
    return top_news