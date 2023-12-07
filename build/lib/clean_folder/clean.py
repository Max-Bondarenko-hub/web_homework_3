import sys
import shutil
from pathlib import Path
import os

# c:\Users\Max\Python\Projects\vs-basics\folder_for_hw

CATEGORIES = {'Soft': ['.exe'],
              'Images': ['.jpg', '.png', '.bmp', '.ico', '.jpeg', '.svg'],
              'Documents': ['.docx', '.pdf', '.txt', '.xlsx', '.djvu', '.doc'],
              'Audio': ['.mp3'],
              'Video': ['.avi', '.mkv', '.mov'],
              'Python': ['.py'],
              'Archives': ['.zip', '.tar', '.gz']}

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ('a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu', 
'ya', 'je', 'i', 'ji', 'g')
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

counter = 1

def get_category(file:Path) -> str:
    exten = file.suffix.lower()
    for c, ex in CATEGORIES.items():
        if exten in ex:
            return c
    return 'Other'

def normalize(name:str) -> str:
    f_name, f_ext = os.path.splitext(name)
    new_f_name = f_name.translate(TRANS)
    final_name = ''
    for el in new_f_name:
        if (not el.isalpha()) and (not el.isdigit()):
            el = '_'
        final_name += el
    final_name += f_ext
    return final_name

def move_f(elem:Path, cat:str, d_path:Path) -> None:
    global counter
    root_dir = d_path.joinpath(cat)
    if not root_dir.exists():
        root_dir.mkdir()
    try:
        elem.rename(root_dir.joinpath(normalize(elem.name)))
    except FileExistsError:
        name, ext = os.path.splitext(elem.name)
        new_name = name + '_' + str(counter) + ext
        counter += 1
        elem.rename(root_dir.joinpath(normalize(new_name)))

def sort_fld(path:Path) -> None:
    for el in path.glob('**/*'):
        if el.is_file():
            category = get_category(el)
            move_f(el, category, path)

def del_empty_dir(path:Path) -> None:
    for el in path.glob('*'):
        if el.is_dir():
            del_empty_dir(el)
            if len(os.listdir(el)) == 0:
                shutil.rmtree(el)

def unpack_achives(path:Path) -> None:
    arch_dir = path.joinpath('Archives')
    if arch_dir.exists():
        for arch in arch_dir.glob('*'):
            if arch.is_file():
                new_arch_dir = arch_dir.joinpath(arch.stem)
                if not new_arch_dir.exists():
                    new_arch_dir.mkdir()
                shutil.unpack_archive(arch, new_arch_dir)
                # os.remove(arch)

def main() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'No path to folder'

    if not path.exists():
        return 'Path does not exists'
    
    sort_fld(path)
    del_empty_dir(path)
    unpack_achives(path)

    return 'Sorting complite!'


if __name__ == '__main__':
    print(main())