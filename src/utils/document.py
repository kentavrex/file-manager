import re
from typing import Iterable


def rreplace(s: str, old: str, new: str, occurrence: int) -> str:
    li = s.rsplit(old, occurrence)
    return new.join(li)


def get_max_suffix(name: str, extension: str, existed_names: Iterable[str]) -> int:
    max_suffix = 0
    for n in existed_names:
        if re.match(pattern=rf"{name}\s\(\d+\){extension}", string=n):
            number = re.findall(pattern=r"\d+", string=n)[-1]
            max_suffix = max(int(number), max_suffix)
    return max_suffix


def split_extension(filename: str) -> tuple[str, str]:
    if "." in filename:
        return filename.split(".")[0], "." + filename.split(".")[-1]
    return filename, ""


def get_new_filename(filename: str, existed_names: Iterable[str]) -> str:
    if filename not in existed_names:
        return filename

    filename_without_extension, extension = split_extension(filename)
    if re.match(pattern=r".+\s\(\d+\)", string=filename_without_extension):
        number = re.findall(pattern=r"\d+", string=filename_without_extension)[-1]
        pure_name = rreplace(filename_without_extension, f" ({number})", "", 1)
        max_suffix = get_max_suffix(pure_name, extension, existed_names)
        return rreplace(filename_without_extension, number, str(max_suffix + 1), 1)

    max_suffix = get_max_suffix(filename_without_extension, extension, existed_names)
    return f"{filename_without_extension} ({max_suffix + 1}){extension}"
