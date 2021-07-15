from pathlib import Path


def only_name(file_path:str):
    file_path = Path(file_path)
    file_name = file_path.name
    file_extension = file_path.suffix

    return file_name[:-len(file_extension)]
