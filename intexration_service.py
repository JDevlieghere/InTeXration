import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-python', help('Python 3'), default='python')
    parser.add_argument('-host', help='Hostname', default='localhost')
    parser.add_argument('-port', help='Port', default=8000)
    args = parser.parse_args()
    subprocess.call(['nohup', args.python, 'intexration.py', '-host', args.host, '-post', args.port])

if __name__ == '__main__':
    main()