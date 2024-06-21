import argparse

from Bilibili_Crawler import Bilibili_Crawler


def main():
    parser = argparse.ArgumentParser(description='Bilibili Crawler.')
    parser.add_argument('-url', type=str)
    args = parser.parse_args()
    bc = Bilibili_Crawler(args.url)
    bc()


if __name__ == '__main__':
    main()
