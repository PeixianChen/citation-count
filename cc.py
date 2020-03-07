from colorama import Style, Fore

from core import GoogleScholar
from settings import ARTICLES, EXPORT
from utils import is_journal, is_others, highlight


def cc(title: str, authors: str):
    with GoogleScholar() as gs:
        # 前往文章搜索页面
        gs.search(title)
        if not gs.search_citations_of_the_1st_result():
            print(Fore.YELLOW + 'No citations found.')
            exit(0)

        # 遍历每一页
        page, total = 0, 0
        while True:

            page += 1
            print('-' * 10)
            print(Style.BRIGHT + Fore.GREEN + 'Page %d' % page)
            print('-' * 10)

            articles = gs.extract_articles_of_current_page()
            for i, cite in enumerate(articles):
                # valid = is_journal(cite)[0] and is_others(cite, authors)[0]
                valid = is_others(cite, authors)[0]
                cite = highlight(cite, authors)
                total += valid

                message = [
                    Fore.BLUE,
                    Style.BRIGHT, '[%02d] %s\n' % (i + 1, cite.title),
                    Style.NORMAL, '     %s\n' % cite.url,
                    Style.NORMAL, '     %s\n' % cite.authors,
                    Style.NORMAL + Fore.YELLOW + '     %s\n' % cite.citations.get(EXPORT, 'Not Found.'),
                    Style.BRIGHT + Fore.MAGENTA + '     Good.\n' if valid else '',
                ]
                print(''.join(message))

            # arg = input('Valid citations %d, press ENTER or input NEW count: ' % total)
            # if arg.isdigit():
            #     total = int(arg)
            #     print('Update citations: %d' % total)

            if not gs.goto_next_page():
                break

    return total


if __name__ == '__main__':
    for title, authors in ARTICLES:
        print('-' * 100)
        print(Style.BRIGHT + Fore.GREEN + title)
        print(Style.NORMAL + Fore.GREEN + authors)
        print('-' * 100)

        total = cc(title, authors)

        print('Total count: ' + Style.BRIGHT + Fore.GREEN + '%d' % total)
