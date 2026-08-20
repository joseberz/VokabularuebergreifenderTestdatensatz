import argparse
import shutil
from pathlib import Path

DATASETS = {
    "pc59": "PC59_novel",
    "idd": "IDD_novel",
    "nyu": "NYU_novel",
}


def build_index(source_dir, rgb_only=False):
    index = {}
    for path in Path(source_dir).rglob("*"):
        if not path.is_file():
            continue
        if rgb_only and "rgb" not in [p.lower() for p in path.parent.parts]:
            continue
        index.setdefault(path.name, path)
    return index


def find(source_dir, index, entry, rgb_only=False):
    candidate = Path(source_dir) / entry
    if candidate.is_file() and (not rgb_only or "rgb" in [p.lower() for p in candidate.parent.parts]):
        return candidate

    name = Path(entry).name
    if name in index:
        return index[name]

    # in dem fall konnte das bild nicht gefunden werden
    stem = Path(entry).stem
    for ext in (".jpg", ".jpeg", ".JPG", ".JPEG"):
        new_name = stem + ext
        if new_name in index:
            return index[new_name]

        new_candidate = Path(source_dir) / (str(Path(entry).with_suffix("")) + ext)
        if new_candidate.is_file() and (not rgb_only or "rgb" in [p.lower() for p in new_candidate.parent.parts]):
            return new_candidate

    return None


def process_dtset(dataset_folder, source_dir, rgb_only=False):
    image_root = Path(dataset_folder) / "image"
    if not image_root.exists():
        print(f"übersprungen weil Ordner nicht existiert")
        return

    index = build_index(source_dir, rgb_only=rgb_only)
    found, missing = 0, 0

    for class_dir in sorted(image_root.iterdir()):
        if not class_dir.is_dir():
            continue
        filelist = class_dir / "filelist.txt"
        if not filelist.exists():
            continue

        entries = [
            line.strip()
            for line in filelist.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        for entry in entries:
            src = find(source_dir, index, entry, rgb_only=rgb_only)

            if src is None:
                missing += 1
                continue

            dst = class_dir / src.name
            shutil.copy2(src, dst)
            found += 1

    print(f"{dataset_folder}: {found} wurden kopiert, {missing} fehlen")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pc59", help="Pfad zum Originalbilder-Ordner von PC59")
    parser.add_argument("--idd", help="Pfad zum Originalbilder-Ordner von IDD")
    parser.add_argument("--nyu", help="Pfad zum Originalbilder-Ordner von NYU")
    args = parser.parse_args()

    sources = {"pc59": args.pc59, "idd": args.idd, "nyu": args.nyu}

    for key, folder in DATASETS.items():
        source_dir = sources[key]
        if not source_dir:
            continue
        if key == "nyu":
            process_dtset(folder, source_dir, rgb_only=True)
        else:
            process_dtset(folder, source_dir, rgb_only=False)


if __name__ == "__main__":
    main()