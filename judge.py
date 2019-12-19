import argparse


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


if __name__ == '__main__':
    args = get_args()
