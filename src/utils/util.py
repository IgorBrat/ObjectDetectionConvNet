import os.path


def count_images_in_directory():
    dir_images = os.getcwd() + '\images\prediction'
    return len([name for name in os.listdir(dir_images) if os.path.isfile(os.path.join(dir_images, name))])
