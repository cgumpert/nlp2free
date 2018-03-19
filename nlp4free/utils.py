from collections import Counter
import matplotlib.pyplot as plt
import operator
import pandas as pd
import re

def profile_corpus(reader,
                   to_lower = True,
                   check_html_tags = True,
                   check_special_chars = True,
                   check_whitespace = True):       
    char_counter = Counter()
    token_counter = Counter()
    bigram_counter = Counter()
    rows = []
    for text in reader:
        # simple normalization
        if to_lower:
            text = text.lower()
        
        # split into tokens
        tokens = re.findall(r'\b\w+\b', text)
        
        # simple counts
        char_counter += Counter(text)
        token_counter += Counter(tokens)
        bigram_counter += Counter(zip(tokens[:-1], tokens[1:]))

        # standard key figures
        text_len = len(text)        
        result = {'text length': text_len,
                  'tokens': len(tokens),
                  'is empty': int(not bool(text.strip()))}
        
        # detailed investigations
        if check_html_tags:
            result['HTML tags'] = len(re.findall(r'<(\w).*>.*</\1>', text))
        
        if check_special_chars:
            n_special_chars = len(re.findall(r'[^\w\s-]|[_\d]', text))
            result['special char fraction'] = n_special_chars / text_len if text_len else 0
        
        if check_whitespace:
            n_whitespaces = len(re.findall(r'\s', text))
            result['whitespace fraction'] = n_whitespaces / text_len if text_len else 0

        rows.append(result)
        
    return char_counter, token_counter, bigram_counter, pd.DataFrame(rows)

def show_corpus_profile(reader,
                        top_n = 20,
                        to_lower = True,
                        check_html_tags = True,
                        check_special_chars = True,
                        check_whitespace = True):
    cc, tc, _, _ = profile_corpus(reader,
                                    to_lower,
                                    check_html_tags,
                                    check_special_chars,
                                    check_whitespace)
    _, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (16,12))
    axes[0][0].set_title('Top %d characters' % top_n)
    axes[1][0].set_title('Last %d characters' % top_n)
    axes[0][1].set_title('Top %d tokens' % top_n)
    axes[1][1].set_title('Last %d tokens' % top_n)
    cc = sorted(cc.items(), key = operator.itemgetter(1), reverse = True)
    tc = sorted(tc.items(), key = operator.itemgetter(1), reverse = True)
    chars, char_counts = zip(*cc)
    tokens, token_counts = zip(*tc)
    pd.Series(char_counts[top_n::-1], index = chars[top_n::-1]).plot.barh(ax = axes[0][0])
    pd.Series(char_counts[-1:-top_n:-1], index = chars[-1:-top_n:-1]).plot.barh(ax = axes[1][0])
    pd.Series(token_counts[top_n::-1], index = tokens[top_n::-1]).plot.barh(ax = axes[0][1])
    pd.Series(token_counts[-1:-top_n:-1], index = tokens[-1:-top_n:-1]).plot.barh(ax = axes[1][1])
    
def flatten(container, max_level = -1):
    for obj in container:
        if max_level != 0  and isinstance(obj, (list, tuple, set)):
            yield from flatten(obj, max_level - 1)
        else:
            yield obj
