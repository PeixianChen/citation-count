from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils import wait_captcha, wait_element, Article


class GoogleScholar(webdriver.Chrome):
    """对 Google Scholar 相关操作的包装
    """

    URL_INDEX = 'https://scholar.google.com'

    def __init__(self, *args, **kwargs):
        super(GoogleScholar, self).__init__(*args, **kwargs)
        self.get(self.URL_INDEX)

    @wait_captcha
    def search(self, keyword: str) -> None:
        try:
            search_bar = self.find_element_by_id('gs_hdr_tsi')
            search_bar.send_keys(keyword)
            search_bar.submit()
        except NoSuchElementException:
            raise Exception('当前页面无法定位搜索栏: %s' % self.current_url)

    @wait_captcha
    def search_citations_of_the_1st_result(self) -> bool:
        """搜索被引文章
        假定搜索目标为当前页面第一篇文章。

        Returns:
            是否被引
        """
        try:
            btn_cited = self.find_element_by_xpath('//a[contains(@href, "/scholar?cites=")]')
            btn_cited.click()
        except NoSuchElementException:
            return False
        return True

    @wait_captcha
    def extract_articles_of_current_page(self) -> List[Article]:
        """提取当前页面所有文章数据
        """
        articles = []
        for div_article in self.find_elements_by_xpath('//div[@class="gs_ri"]'):
            # 文章信息
            try:
                lnk_article = div_article.find_element_by_xpath('./h3/a')
                title, url = map(lnk_article.get_attribute, ['text', 'href'])
            except NoSuchElementException:
                # 忽略异常文章
                title, url = 'Not Available', 'Not Available'

            # 作者信息
            try:
                div_authors = div_article.find_element_by_xpath('./div[@class="gs_a"]')
                authors = div_authors.text
            except NoSuchElementException:
                authors = 'Not Available'

            # 引用源
            try:
                citations = self.extract_citations(div_article)
                import time
                time.sleep(3)
            except:
                citations = dict()

            articles.append(Article(title, url, authors, citations))

        return articles

    def extract_citations(self, div_article) -> dict:
        """提取某文章的引用格式
        """
        # 打开引用表格
        btn_citation = div_article.find_element_by_xpath('./div/a[@class="gs_or_cit gs_nph"]')
        btn_citation.click()

        # 检索引用表格
        tab_citation = wait_element(self, '//div[@id="gs_citt"]')
        citations = tab_citation.text.split('\n')
        citations = dict(zip(citations[0::1], citations[1::1]))

        # 关闭引用表格
        btn_close = wait_element(self, '//a[@id="gs_cit-x"]')
        btn_close.click()

        return citations

    @wait_captcha
    def goto_next_page(self) -> bool:
        """前往下一页

        Returns:
            是否存在下一页
        """
        try:
            btn_next = self.find_element_by_xpath('//div[@id="gs_n"]//td[@align="left"]')
            if not btn_next.text:
                return False
        except NoSuchElementException:
            return False

        btn_next.click()
        return True

    @wait_captcha
    def get(self, url):
        super(GoogleScholar, self).get(url)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
