import datetime
import logging
import os


DIVISOR_LENGTH = 80
FILE_AGE_TO_DELETE_IN_DAYS = datetime.timedelta(days=1)


def remove_files_by_extension(directory: str, file_extension: str, remove_file_by_age: bool = True):
    logging.info(f'Removing {file_extension.upper()} files from {directory}')

    files_with_specific_extension = list(os.path.join(directory, file) for file in os.listdir(directory)
                                         if file.endswith(file_extension))
    remove_files(files_with_specific_extension, remove_file_by_age)


def empty_directory(start_directory: str, remove_file_by_age: bool = True):
    sub_directories = list(directory[0] for directory in os.walk(start_directory))
    for directory in reversed(sub_directories):
        logging.info(f'Cleanning {directory}')
        files_in_folder = get_files_in_directory(directory)
        remove_files(files_in_folder, remove_file_by_age)
        if directory_is_empty(directory) and (directory != start_directory):
            os.rmdir(directory)


def remove_files(files: list, check_file_age: bool):
    removed_file_count = 0
    current_date = datetime.datetime.now().date()
    for file in files:
        file_modification_date = datetime.datetime.fromtimestamp(os.path.getmtime(file)).date()
        if check_file_age:
            if ((current_date - file_modification_date) > FILE_AGE_TO_DELETE_IN_DAYS):
                os.remove(file)
                removed_file_count += 1
        else:
            os.remove(file)
            removed_file_count += 1

    logging.info(f'Removed {removed_file_count} files')
    logging.info('=' * DIVISOR_LENGTH)


def directory_is_empty(directory: str) -> bool:
    return not os.listdir(directory)


def get_files_in_directory(directory: str) -> list:
    files = list(os.path.join(directory, file) for file in os.listdir(directory))
    return list(file for file in files if os.path.isfile(file))


def log_initialization():
    log_file_path = os.path.expanduser('~') + '\\Desktop\\clean_files.log'
    if (os.path.exists(log_file_path)):
        os.remove(log_file_path)

    logging.basicConfig(filename=log_file_path, level=logging.INFO)


def main():
    log_initialization()
    # empty_directory deletes all files in a directory and the directory itself if it is empty after remove all files
    # Parameters:
    #       path_to_be_clean = Str
    #       remove_file_by_age = Bool -> Default: True (delete files older than 1 day).
    empty_directory('C:\\lixo\\', False)

    # remove_files_by_extension delete all files (only the files)  of a certain extension
    # .Paraeters:
    #       directory = Str -> the main diectory you want to clean.
    #       file_extension = Str -> the file type you want to delete (txt, log, ...)
    #       remove_file_by_age = Bool -> Default: True (delete files older than 1 day).
    remove_files_by_extension('D:\\TEX\\MOL\\', 'log', False)


if __name__ == "__main__":
    main()
