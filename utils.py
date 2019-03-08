from collections import namedtuple
from functools import wraps

from colorama import Fore
from selenium.webdriver.support.expected_conditions import url_matches
from selenium.webdriver.support.wait import WebDriverWait

from settings import JOURNAL_WHITELIST, JOURNAL_BLACKLIST, EXCLUSIVE_AUTHORS

Article = namedtuple('Article', 'title url authors')


def wait_captcha(func):
    """对可能引发验证码的函数进行延时
    """
    timeout, pattern = 600, r'^https://scholar'  # FIXME: 判断元素加载状态，以等待页内验证码

    @wraps(func)
    def wrapped_func(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        WebDriverWait(self, timeout).until(url_matches(pattern))
        return res

    return wrapped_func


def is_journal(article: Article):
    """判断是否为期刊的逻辑

    Args:
        article: 文章

    Returns:
        判断结果，和相关的关键词
    """
    # 白名单
    for keyword in JOURNAL_WHITELIST:
        if keyword in article.url:
            return True, keyword

    # 黑名单
    for keyword in JOURNAL_BLACKLIST:
        if keyword in article.url:
            return False, keyword

    # 默认为期刊
    return True, None


def is_others(article: Article, authors: str):
    """判断是否为他引的逻辑

    Args:
        article: 文章
        authors: 引用文章作者

    Returns:
        判断结果，和相关的作者姓名
    """
    exclusive = map(lambda s: s.strip(), authors.split(',') + EXCLUSIVE_AUTHORS)
    cite_by = map(lambda s: s.strip().strip('…'), article.authors.split(' - ')[0].split(','))
    for name in exclusive:
        if name in cite_by:
            return False, name
    return True, None


def highlight(article: Article, authors: str):
    """高亮

    Args:
        article: 待高亮文章
        authors: 引用文章作者

    Returns:
        高亮后待文章
    """
    valid, keyword = is_journal(article)
    if keyword is not None:
        color = Fore.GREEN if valid else Fore.RED
        new_url = article.url.replace(keyword, color + keyword + Fore.BLUE)
        article = article._replace(url=new_url)

    valid, name = is_others(article, authors)
    if name is not None:
        new_authors = article.authors.replace(name, Fore.RED + name + Fore.BLUE)
        article = article._replace(authors=new_authors)

    return article
