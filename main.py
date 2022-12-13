import datetime
import json
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


def get_parameters() -> dict:
    parameter_file = os.path.dirname(__file__) + '\\parameters.json'
    if not os.path.exists(parameter_file):
        logging.error(f'File \"parameters.json\" not found in directory {os.path.dirname(__file__)}')
        exit()

    with open(parameter_file) as parameter_file:
        return json.load(parameter_file)


def valid_parameter_file(parameters: dict) -> bool:
    if not list(parameters.keys())[0] == 'directories':
        logging.error('Error: Parameter \"directories\" not found')
        exit()

    parameter_order = 0
    for parameter in parameters['directories']:
        parameter_order += 1
        if not 'path' in parameter:
            logging.error(f'Error: Parameter \"path\" not found. Parameter {parameter_order}.')
            exit()
        if not 'remove_by_age' in parameter:
            logging.error(f'Error: Parameter \"remove_bay_age\" not found. Parameter {parameter_order}.')
            exit()

    return True


def main():
    log_initialization()

    parameters = get_parameters()
    if not valid_parameter_file(parameters):
        exit()

    for parameter in parameters['directories']:
        if 'file_extension' in parameter:
            remove_files_by_extension(parameter['path'], parameter['file_extension'], parameter['remove_by_age'])
        else:
            empty_directory(parameter['path'], parameter['remove_by_age'])


if __name__ == "__main__":
    main()
