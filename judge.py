import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data-dir',
        help='Put zip files from ceiba in the directory'
    )
    parser.add_argument(
        '--answer-link',
        help='TA reference answer link.'
    )
    args = parser.parse_args()
    return args

print(get_args())
