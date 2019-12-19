import argparse
import os
import requests
import sys
import zipfile
from pathlib import Path
from time import sleep
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
    parser.add_argument(
        '--unzip-dir',
        default='./files',
        help='The unzip file save directory name'
    )
    parser.add_argument(
        '--output',
        default='score.csv',
        help='The output score csv file.'
    )
    args = parser.parse_args()
    return args


class Error:
    class PaizaParserError(Exception):
        pass

    class ParseAnswerError(Exception):
        pass
            
    class AnswerCheckerError(Exception):
        pass


class PaizaParser:
    @staticmethod
    def get_hash(url):
        return urlparse(url).path
        
    @classmethod
    def get_answer_url(cls, url):
        answer_url = f'https://out.paiza.io{cls.get_hash(url)}/output.txt'
        return answer_url

    @classmethod
    def get_answer(cls, url):
        res = requests.get(cls.get_answer_url(url))
        sleep(0.5)
        if res.status_code != 200:
            raise Error.PaizaParserError(
                f'Possible wrong link is given "{url}" '
                f'with status code {res.status_code}.')
        answer_text = res.text
        answer = AnswerParser.parse_answer_text(answer_text)
        return answer


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
            raise Error.ParseAnswerError(
                f'Possible wrong output format. Get {q_count} queries')
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


class AnswerChecker:
    def __init__(self, root_path, save_csv, answer_link, answer_func):
        self.p = root_path
        self.sp = save_csv
        self.answer = answer_func(answer_link)
        self.answer_func = answer_func

    @staticmethod
    def parse_url_from_file(fn):
        try:
            with open(fn, 'r') as f:
                return f.readline().strip()
        except:
            raise Error.AnswerCheckerError(f'Cannot open file {fn}')
                        
    def parse_answer_from_file(self, fn):
        try:
            with open(fn, 'r') as f:
                content = f.read()

            answer = AnswerParser.parse_answer_text(content)
            return answer
        except:
            raise Error.AnswerCheckerError(f'Cannot open file {fn}')

    @staticmethod
    def check_answer_score(correct_answer, answer, fn_answer, accum=20):
        total_score = 0
        for q_1, q_2, q_3 in zip(correct_answer, answer, fn_answer):
            if q_1 == q_2 == q_3:
                total_score += accum
        return total_score

    def check(self):
        p = Path(self.p)
        with open(self.sp, 'w') as f:
            for dir_name in p.glob('*'):
                if dir_name.is_dir():
                    name = dir_name.name
                    score = 0
                    print(f'Processing {name}', file=sys.stderr)
                    try:
                        url_fn = dir_name.joinpath(dir_name.name + '.txt')
                        url = self.parse_url_from_file(url_fn)
                        out_fn = dir_name.joinpath('output.txt')
                        fn_answer = self.parse_answer_from_file(out_fn)
                        answer = self.answer_func(url)
                        score += self.check_answer_score(
                            self.answer, answer, fn_answer)
                        self.write_to_csv(
                            f, name, score, '')
                    except Error.PaizaParserError as e:
                        self.write_to_csv(f, name, score, e)
                    except Error.AnswerCheckerError as e:
                        self.write_to_csv(f, name, score, e)
                    except Error.ParseAnswerError as e:
                        self.write_to_csv(f, name, score, e)
    
    @staticmethod
    def write_to_csv(f, name, score, msg):
        out = f'{name},{score},{msg}\n'
        f.write(out)


if __name__ == '__main__':
    args = get_args()
    dp = DataProcessor(args.data_dir, args.unzip_dir)
    dp.unzip_files()
    ac = AnswerChecker(
        args.unzip_dir,
        args.output,
        args.answer_link,
        PaizaParser.get_answer
    )
    ac.check()
