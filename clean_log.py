import argparse
import logging
from typing import Optional

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Sanitizer(logging.Formatter):
    def __init__(self, *args, filter_vals: Optional[list] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._filter_vals = filter_vals or []

    def _sanitize(self, val: str):
        result: str = val or ''
        for val in self._filter_vals:
            result = result.replace(val, '********')
        return result

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._sanitize(original)


def configure_logging():
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)
    log.propagate = False


def main(value: str) -> str:
    for handler in log.handlers:
        handler.setFormatter(
            Sanitizer(
                filter_vals=[
                    'sanitized',
                ]
            )
        )

    result: str = value
    log.info(value)
    return result


if __name__ == '__main__':
    configure_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--value',
        type=str,
        required=True,
        help="The value you want to clean.",
    )

    clargs = parser.parse_args()

    if data := main(clargs.value):
        print(data)
    else:
        print('No result')
