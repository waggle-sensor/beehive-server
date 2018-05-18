import argparse
from glob import glob
import hashlib
import datetime
import os
import gzip
import multiprocessing
import subprocess
import time


def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read()


def read_compressed_file(filename):
    return gzip.decompress(read_file(filename))


def ensure_dir(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


def hash_dependencies(filenames):
    hash = hashlib.sha1()

    for filename in sorted(filenames):
        with open(filename, 'rb') as file:
            hash.update(file.read())

    return hash.digest()


def get_checkpoint(target):
    try:
        with open(target + '.checkpoint', 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return bytes()


def set_checkpoint(target, hash):
    ensure_dir(target)

    with open(target + '.checkpoint', 'wb') as file:
        file.write(hash)


def find_data_files(top, rel=''):
    for entry in os.scandir(top):
        if entry.is_dir():
            yield from find_data_files(entry, os.path.join(rel, entry.name))
        if entry.is_file() and entry.name.endswith('.csv.gz'):
            yield os.path.join(rel, entry.name)


def update_filtered_files(data_dir, build_dir):
    tasks = []

    for file in find_data_files(data_dir):
        target = os.path.join(build_dir, file)
        dependencies = [os.path.join(data_dir, file)]
        tasks.append((target, dependencies))

    with multiprocessing.Pool() as pool:
        pool.starmap(update_filtered_file_if_needed, tasks)


def update_filtered_file_if_needed(target, dependencies):
    hash = hash_dependencies(dependencies)

    if get_checkpoint(target) == hash:
        return

    print('make', target)
    start = time.time()
    update_filtered_file(target, dependencies)
    print('done', target, time.time() - start)
    set_checkpoint(target, hash)


def update_filtered_file(target, dependencies):
    ensure_dir(target)

    with open(target, 'wb') as outfile:
        for source in dependencies:
            lines = read_compressed_file(source).splitlines()

            # drop header from staged data
            if lines[0].startswith(b'timestamp'):
                lines = lines[1:]

            lines.sort()
            data = b'\n'.join(lines)
            outfile.write(gzip.compress(data))


def update_date_files(data_dir, build_dir):
    tasks = {}

    for file in find_data_files(data_dir):
        date = os.path.basename(file).rstrip('.csv.gz')
        target = os.path.join(build_dir, '{}.csv.gz'.format(date))
        if target not in tasks:
            tasks[target] = []
        tasks[target].append(os.path.join(data_dir, file))

    tasks = sorted(tasks.items(), reverse=True)

    for target, dependencies in tasks:
        update_date_file_if_needed(target, dependencies)


def update_date_file_if_needed(target, dependencies):
    hash = hash_dependencies(dependencies)

    if get_checkpoint(target) == hash:
        return

    print('make', target)
    start = time.time()
    update_date_file(target, dependencies)
    print('done', target, time.time() - start)
    set_checkpoint(target, hash)


# NOTE can also probably load all into memory as a GzipFile and stream the
# lines for merging.
# NOTE may be able to use heap to efficiently do the k way merge
# can insert keys with ref of file read next line from
def update_date_file(target, dependencies):
    update_date_file_memsort(target, dependencies)


def update_date_file_memsort(target, dependencies):
    rows = []

    for source in dependencies:
        rows.extend(read_compressed_file(source).splitlines())

    rows.sort()

    data = gzip.compress(b'\n'.join(rows))

    ensure_dir(target)

    with open(target, 'wb') as file:
        file.write(data)


def update_date_file_merge(target, dependencies):
    raise NotImplementedError('Still need to prototype and profile.')


# NOTE faster to cat rather than check if needed
def update_combined_file(data_dir, build_dir):
    target = os.path.join(build_dir, 'data.csv.gz')
    dependencies = [os.path.join(data_dir, file) for file in sorted(find_data_files(data_dir))]

    print('make', target)
    start = time.time()

    with open(target, 'wb') as file:
        # restore header to final result
        header = b'timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf\n'
        file.write(gzip.compress(header))

        for dep in dependencies:
            file.write(read_file(dep))

    print('done', target, time.time() - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir')
    parser.add_argument('build_dir')
    args = parser.parse_args()

    data_dir = os.path.abspath(args.data_dir)
    build_dir = os.path.abspath(args.build_dir)
    filtered_dir = os.path.join(build_dir, 'filtered')
    dates_dir = os.path.join(build_dir, 'dates')

    update_filtered_files(data_dir, filtered_dir)
    update_date_files(filtered_dir, dates_dir)
    update_combined_file(dates_dir, build_dir)
