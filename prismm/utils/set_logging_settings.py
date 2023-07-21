import logging
import sys

def set_logging_settings(args):
    logging.basicConfig(stream=sys.stdout)  # initialize basicConfig first
    logger = logging.getLogger()
    
    if args.debug == "debug":
        logger.setLevel(logging.DEBUG)
    elif args.debug == "info":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

