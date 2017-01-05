from look_viewer import util


def test_iterate_subfolders(tmp_path):
    folders_to_create = ["folder_1", "folder_2"]
    files_to_create = ["file_1.png", "file_2.jpg", "file_3.gif"]
    _create_folders(tmp_path, folders_to_create)
    _create_files(tmp_path, files_to_create)
    subfolders = sorted(util.iterate_subfolders(tmp_path))
    assert subfolders == sorted(folders_to_create)


def _create_folders(folder, folder_names):
    for subfolder in folder_names:
        os.mkdir(os.path.join(folder, subfolder))


def _create_files(folder, file_names):
    for file_name in file_names:
        with open(os.path.join(folder, file_name), "w") as fout:
            pass
