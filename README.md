# citation-count
基于 Google Scholar 的论文他引次数统计。

## Usage
```sh
cd citation-count
pip install -r requirements.txt
cp settings.sample.py settings.py
python cc.py
```

## Configure
* `JOURNAL_WHITELIST` 判定为**期刊**的关键词，如 `ieee` 等。
* `JOURNAL_BLACKLIST` 判定为**非期刊**的关键词，如 `arxiv` 等。
* `EXCLUSIVE_AUTHORS` 不计入**他引**的作者名单，可随意设置。
* `ARTICLES` 待处理的文章列表
* 自行确认并修改 `utils.py` 中的判定逻辑 `is_journal` 和 `is_others`。
