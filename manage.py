import argparse
from todo import app
from todo.models import init


def run():
    app.run(host='127.0.0.1', port=5000, debug=True)


def init_db():
    init()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    subparsers.required = True

    foo_parser = subparsers.add_parser("run")
    foo_parser.set_defaults(fn=run)

    bar_parser = subparsers.add_parser("init_db")
    bar_parser.set_defaults(fn=init_db)

    args = parser.parse_args()
    args.fn()
