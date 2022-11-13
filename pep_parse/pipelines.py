import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILENAME = 'status_summary_{now_format}.csv'


class PepParsePipeline:
    def __init__(self):
        self.result_dir = BASE_DIR / 'results'
        self.result_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.results = defaultdict(int)

    def process_item(self, item, spider):
        self.results[item['status']] += 1
        return item

    def close_spider(self, spider):
        now = dt.datetime.now()
        now_format = now.strftime(DATETIME_FORMAT)
        filename = FILENAME.format(now_format=now_format)
        file_path = self.result_dir / filename
        with open(file_path, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(
                csvfile,
                dialect=csv.unix_dialect,
                quoting=csv.QUOTE_MINIMAL
            )
            writer.writerows([
                ('Статус', 'Количество'),
                *self.results.items(),
                ('Total', sum(self.results.values()))
            ])
