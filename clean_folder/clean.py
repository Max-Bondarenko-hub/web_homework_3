import sys
import shutil
from pathlib import Path
import os
import time
import Trans
from threading import Thread


CATEGORIES = {
    "Soft": [".exe"],
    "Images": [".jpg", ".png", ".bmp", ".ico", ".jpeg", ".svg"],
    "Documents": [".docx", ".pdf", ".txt", ".xlsx", ".djvu", ".doc", "mobi", ".pptx"],
    "Audio": [".mp3", ".m4a"],
    "Video": [".avi", ".mkv", ".mov"],
    "Python": [".py"],
    "Archives": [".zip", ".tar", ".gz"],
    "System": [".dll", ".ini", ".reg"],
}

CYRILLIC_SYMBOLS = Trans.CYRILLIC_SYMBOLS
TRANSLATION = Trans.TRANSLATION

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

counter = 1


class MyThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs


    def run(self) -> None:    
        elem = self.args[0]
        cat = self.args[1]
        d_path = self.args[2]
        global counter
        root_dir = d_path.joinpath(cat)
        if not root_dir.exists():
            root_dir.mkdir()
        try:
             elem.rename(root_dir.joinpath(normalize(elem.name)))
        except FileExistsError:
            name, ext = os.path.splitext(elem.name)
            new_name = name + "_" + str(counter) + ext
            counter += 1
            elem.rename(root_dir.joinpath(normalize(new_name)))




def get_category(file: Path) -> str:
    exten = file.suffix.lower()
    for c, ex in CATEGORIES.items():
        if exten in ex:
            return c
    return "Other"


def normalize(name: str) -> str:
    f_name, f_ext = os.path.splitext(name)
    new_f_name = f_name.translate(TRANS)
    final_name = ""
    for el in new_f_name:
        if (not el.isalpha()) and (not el.isdigit()):
            el = "_"
        final_name += el
    final_name += f_ext
    return final_name


def sort_fld(path: Path) -> None:
    for el in path.glob("**/*"):
        if el.is_file():
            category = get_category(el)
            thread = MyThread(args=(el, category, path))
            thread.start()


def del_empty_dir(path: Path) -> None:
    for el in path.glob("*"):
        if el.is_dir():
            del_empty_dir(el)
            if len(os.listdir(el)) == 0:
                shutil.rmtree(el)


def unpack_achives(path: Path) -> None:
    arch_dir = path.joinpath("Archives")
    if arch_dir.exists():
        for arch in arch_dir.glob("*"):
            if arch.is_file():
                new_arch_dir = arch_dir.joinpath(arch.stem)
                if not new_arch_dir.exists():
                    new_arch_dir.mkdir()
                shutil.unpack_archive(arch, new_arch_dir)


def main() -> str:
    start_time = time.time()
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Path does not exists"

    sort_fld(path)
    del_empty_dir(path)
    unpack_achives(path)

    print("--- %s seconds ---" % (time.time() - start_time))

    return "Sorting complite!"


if __name__ == "__main__":
    print(main())
