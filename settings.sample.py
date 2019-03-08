from colorama import init

init(autoreset=True)

# 期刊白名单
JOURNAL_WHITELIST = ['sciencedirect', 'ieee', 'springer', 'aaai']

# 期刊黑名单
JOURNAL_BLACKLIST = ['arxiv']

# 不计入他引的作者名单
EXCLUSIVE_AUTHORS = [
    'Name A',
    'Name B'
]

# 待检测文章列表
ARTICLES = [
    ('TITLE A', 'AUTHOR AA, AUTHOR AB, ...'),
    ('TITLE B', 'AUTHOR BA, AUTHOR BB, ...'),
]
