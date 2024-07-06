"""Module to create and populate files with randomly generated text in the specific folder"""

import os
from faker import Faker

FILES = 50
LENGTH = 1000
DIRECTORY = "src"

fake = Faker()


def main(num_files: int = FILES, text_length: int = LENGTH, directory: str = DIRECTORY):
    """
    Function to create a directory and populate it with files with fake text

    :param num_files: Number of files with randomly generated text to be created
    :param text_length: Length of the randomly generated text
    :param directory: Name of the directory to be created and populated with files
    :return: None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(num_files):
        file_path = os.path.join(directory, f"file{i + 1}.txt")
        with open(file_path, "w", encoding="UTF-8") as fd:
            fd.write(fake.text(max_nb_chars=text_length))

    print(f"Seeded {num_files} files with random text in the '{directory}' directory")


if __name__ == "__main__":
    main()
