import argparse
from configargparse import ArgumentParser

from wikiracer.app.event import event_rec

parser = ArgumentParser(
    allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('-o', '--origin', default='wikipedia.org',
                    help='Origin')
parser.add_argument('-s', '--start', default='/wiki/Battle_of_Cr%C3%A9cy',
                    help='URL we start with')
parser.add_argument('-f', '--finish', default='/wiki/Sweden',
                    help='Our finish URL')


def main():
    args = parser.parse_args()

    init_dct = {
        args.start: {
            'depth': 0,
            'parent': args.start,
            'parsed': False
        }
    }

    # Because of recursion we cant pass just args
    end_url = args.finish
    origin_url = args.origin

    event_rec(init_dct, end_url, origin_url)


if __name__ == '__main__':
    main()
