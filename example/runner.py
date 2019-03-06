import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def runner(app):
    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter,
        description='Starts the example app',
    )
    parser.add_argument('-H', '--host', default='0.0.0.0')
    parser.add_argument('-p', '--port', default=5000)
    parser.add_argument('-l', '--logfile')
    args = parser.parse_args()
    if args.logfile is not None:
        file_handler = logging.FileHandler(args.logfile)
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)
    app.run(host=args.host, port=args.port)
