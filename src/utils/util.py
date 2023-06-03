import os
import os.path
import shutil


def count_images_in_directory():
    dir_images = os.getcwd() + '\images\prediction'
    return len([name for name in os.listdir(dir_images) if os.path.isfile(os.path.join(dir_images, name))])


def clear_directory(directory: str):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
