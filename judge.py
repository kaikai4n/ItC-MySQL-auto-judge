import argparse
import os
import requests
import zipfile
from urllib.parse import urlparse
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data-dir',
        required=True,
        help='Put zip files from ceiba in the directory'
    )
    parser.add_argument(
        '--answer-link',
        required=True,
        help='TA reference answer link.'
    )
    parser.add_argument(
        '--unzip-dir',
        default='./files',
        help='The unzip file save directory name'
    )
    args = parser.parse_args()
    return args


class Error:
    class ParseAnswerError(Exception):
        pass


class PaizaParser:
    @staticmethod
    def get_hash(url):
        return urlparse(url).path
        
    @classmethod
    def get_answer_url(cls, url):
        answer_url = f'https://out.paiza.io{cls.get_hash(url)}/output.txt'
        return answer_url


class AnswerParser:
    @staticmethod
    def get_line_gen(text):
        for one_text in text.split('\n'):
            yield one_text

    @classmethod
    def parse_answer_text(cls, text, total_queries=5):
        answers = [set() for _ in range(total_queries)]
        text_gen = cls.get_line_gen(text)
        q_count = 0
        while True:
            next_q = f'Q{q_count + 1}:'
            try:
                next_line = next(text_gen)
            except StopIteration:
                break
            next_line = next_line.strip()
            if not next_line:
                continue
            if next_q == next_line:
                q_count += 1
                continue
            answers[q_count - 1].add(next_line)
        if q_count != total_queries:
            raise Error.ParseAnswerError(f'Get {q_count} queries')
        return answers


class DataProcessor:
    def __init__(self, path, save_path):
        self.p = path
        self.sp = save_path
        sp_p = os.path.dirname(self.sp)
        if not os.path.isdir(sp_p):
            os.makedirs(sp_p)

    def unzip_files(self):
        p = Path(self.p)
        for fn in p.glob('**/*.zip'):
            with zipfile.ZipFile(str(fn), 'r') as zip_ref:
                zip_ref.extractall(self.sp)


if __name__ == '__main__':
    args = get_args()
    answer_text = requests.get(PaizaParser.get_answer_url(args.answer_link)).text
    answer = AnswerParser.parse_answer_text(answer_text)
    dp = DataProcessor(args.data_dir, args.unzip_dir)
    dp.unzip_files()
    import pdb
    pdb.set_trace()
    pass
