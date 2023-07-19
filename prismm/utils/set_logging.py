import logging

def set_logging(args):
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=level)