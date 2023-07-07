import argparse
import logging
import re

__version__ = '1.0.0.dev'

PATH_LIST_SEPARATOR = ','
PATHS_TO_PATTERN_SEPARATOR = ':'
DEFAULT_PATHS_TO_KEEP_OURS = []
DEFAULT_LOGLEVEL = 'WARNING'
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
PRETTY_PRINT_LOG_LEVELS = ', '.join(LOG_LEVELS)


def configure_logger():
    logger = logging.getLogger()
    # Set basicConfig() to get levels less than WARNING running in our logger.
    # See https://stackoverflow.com/questions/56799138/python-logger-not-printing-info
    # logging.basicConfig(level=logging.WARNING)
    logging.basicConfig(level=logging.INFO)
    # Set a useful logging-format. Not the most elegant way, but it works.
    logger.handlers[0].setFormatter(
        # logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(funcName)s(): %(message)s'))
        # logging.Formatter('%(asctime)s:%(levelname)s:%(module)s:%(funcName)s %(message)s'))
        # logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s %(message)s'))
        logging.Formatter('%(asctime)s:%(levelname)s:Merge-Driver: %(message)s'))
    # See also https://docs.python.org/3/howto/logging.html:
    # numeric_level = self.effective_config.get('loglevel')
    # The check for valid values have been done in parser.add_argument().
    # self.log.setLevel(numeric_level)

    return logger


def parse_command_line_arguments():
    parser = \
        argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                description="TODO description")
    parser.add_argument('-O', '--base', required=True,
                        help="Base version (ancestor's version). Set by Git in %O.")
    parser.add_argument('-A', '--ours', required=True,
                        help="Ours version (current version). Set by Git in %A.")
    parser.add_argument('-B', '--theirs', required=True,
                        help="Theirs version (other branches' version). Set by Git in %B")
    parser.add_argument('-P', '--path',
                        help="The pathname in which the merged result will be stored. Set by Git in %P.")
    parser.add_argument('-p', '--pathpatterns', nargs='+', metavar='PATH:PATTERN',
                        help=f"Paths as regex-patterns to keep ours, separated by {PATHS_TO_PATTERN_SEPARATOR}.")
    parser.add_argument('-o', '--stdout', action='store_true', default=False,
                        help="Print the merge result to stdout rather than to -A/--ours." +
                             " Can be used for evaluating merge scenarios and for testing.")
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-l', '--loglevel', choices=LOG_LEVELS,
                        help=f"Log-level. Defaults to {DEFAULT_LOGLEVEL}.")

    return parser


def get_paths_and_patterns(from_environment_as_str, from_cl_args_as_list):
    # None vs. emtpy string '': Allow switching off defaults or values set by command line by an empty
    # configuration set by environment variable.
    if from_environment_as_str is not None:
        parts = re.split(PATH_LIST_SEPARATOR, from_environment_as_str)
        path_and_pattern_list = [path_and_pattern.strip() for path_and_pattern in parts if path_and_pattern.strip()]
    elif from_cl_args_as_list:
        path_and_pattern_list = [path_and_pattern.strip() for path_and_pattern in from_cl_args_as_list if
                                 path_and_pattern.strip()]
    else:
        return None

    all_paths_and_patterns = []
    for path_and_pattern in path_and_pattern_list:
        path, pattern = split_into_path_and_pattern(path_and_pattern)
        all_paths_and_patterns.append({'path': path, 'pattern': pattern})

    return all_paths_and_patterns


def split_into_path_and_pattern(path_and_pattern):
    if not path_and_pattern:
        return '', ''

    parts = re.split(PATHS_TO_PATTERN_SEPARATOR, path_and_pattern)
    if not parts:
        return []
    value_exception_msg = f"Format error in path pattern '{path_and_pattern}'. Expect 'mandatory-path:optional-pattern."
    if len(parts) > 2:
        raise ValueError(value_exception_msg)

    path = parts[0].strip()
    if not path:
        raise ValueError(value_exception_msg)

    pattern = ''
    if len(parts) == 2:
        pattern = parts[1].strip()

    return path, pattern
