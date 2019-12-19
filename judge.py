import argparse
import requests
from urllib.parse import urlparse


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
    args = parser.parse_args()
    return args


class PaizaParser:
    @staticmethod
    def get_hash(url):
        return urlparse(url).path
        
    @classmethod
    def get_answer_url(cls, url):
        answer_url = f'https://out.paiza.io{cls.get_hash(url)}/output.txt'
        return answer_url


if __name__ == '__main__':
    args = get_args()
    answer_text = requests.get(PaizaParser.get_answer_url(args.answer_link)).text
