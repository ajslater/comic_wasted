#!/usr/bin/env python3
import os
import zipfile
from pathlib import Path
from pprint import pprint

ACCEPTABLE_FNS = "comicinfo.xml"


def record_ext(exts, info):
    ext = Path(info.filename).suffix
    if ext not in exts:
        exts[ext] = 0
    exts[ext] += info.compress_size


def main(comic_root):
    num_archives = 0
    num_extra_files = 0
    total_wasted = 0
    exts = {}
    for root, _, filenames in os.walk(comic_root):
        filenames.sort()
        root_path = Path(root)
        for fn in filenames:
            path = root_path / Path(fn)
            if not zipfile.is_zipfile(path):
                continue
            extra_infos = []
            with zipfile.ZipFile(path) as zf:
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    lower_name = info.filename.lower()
                    if (
                        lower_name.endswith("jpg")
                        or lower_name.endswith("jpeg")
                        or lower_name.endswith("png")
                        or lower_name in ACCEPTABLE_FNS
                    ):
                        continue
                    extra_infos.append(info)
            if extra_infos:
                print(path)
                for info in extra_infos:
                    print("\t", info.filename, info.compress_size)
                    total_wasted += info.compress_size
                    num_extra_files += 1
                    record_ext(exts, info)
                num_archives += 1
    print(
        f"{num_extra_files} extra files in {num_archives} using {total_wasted} compressed bytes."
    )
    print("File extensions:")
    pprint(exts)


if __name__ == "__main__":
    import sys

    comic_root = sys.argv[1]
    main(comic_root)
