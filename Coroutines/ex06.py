import asyncio
import datetime
import errno
import os
import sys

def rotate_file(path, n_versions):
    """Create .1 .2 .3 etc. copies of the specified file."""

    if not os.path.exists(path):
        return
    for i in range(n_versions, 1, -1):
        old_path = "{0}.{1}".format(path, i - 1)
        if os.path.exists(old_path):
            os.rename(old_path, "{0}.{1}".format(path, i))
    os.rename(path, path + ".1")


@asyncio.coroutine
def rotate_by_interval(path, keep_versions, rotate_secs):
    """Rotate file every N seconds."""

    while True:
        yield from asyncio.sleep(rotate_secs)
        rotate_file(path, keep_versions)


@asyncio.coroutine
def rotate_daily(path, keep_versions):
    """Rotate file every midnight."""

    while True:
        now = datetime.datetime.now()
        last_midnight = now.replace(hour=0, minute=0, second=0)
        next_midnight = last_midnight + datetime.timedelta(1)
        yield from asyncio.sleep((next_midnight - now).total_seconds())
        rotate_file(path, keep_versions)


@asyncio.coroutine
def rotate_by_size(path, keep_versions, max_size, check_interval_secs):
    """Rotate file when it exceeds N bytes checking every M seconds."""

    while True:
        yield from asyncio.sleep(check_interval_secs)
        try:
            file_size = os.stat(path).st_size
            if file_size > max_size:
                rotate_file(path, keep_versions)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise


def main(argv):

    loop = asyncio.get_event_loop()
    # Would normally read this from a configuration file.
    rotate1 = loop.create_task(rotate_by_interval("/tmp/file1", 3, 30))
    rotate2 = loop.create_task(rotate_by_interval("/tmp/file2", 5, 20))
    rotate3 = loop.create_task(rotate_by_size("/tmp/file3", 3, 1024, 60))
    rotate4 = loop.create_task(rotate_daily("/tmp/file4", 5))
    loop.run_forever()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
