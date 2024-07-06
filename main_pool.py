"""Module for comparing the performance of multi-threaded and multi-process searches using Pools"""

import os
import time

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from seed import DIRECTORY


def search_keywords_in_files(args: tuple[list, list]) -> dict:
    """
    Function to search for keywords in specific files and add filenames to a common
    queue if a keyword is found in the file

    :param args: Tuple that contains a list of text files to search for keywords
    and a list of keywords to search in files
    :return: Dictionary where keyword is a key and a list of files where
    that word is found as a value
    """
    files, keywords = args
    results = {keyword: [] for keyword in keywords}
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        results[keyword].append(file)
        except (
                FileNotFoundError,
                IsADirectoryError,
                PermissionError,
                UnicodeDecodeError,
            ) as err:
            print(f"Error processing file {file}: {err}")
    return results


def multithreaded_search(split_files: list[list,], keywords: list[str,]):
    """
    Function that provides a multi-threaded search for keywords in files

    :param split_files: Collection of several lists of text files to search for keywords
    :param keywords: List of keywords to search in files
    :return: Iterator with dictionaries where keyword is a key and a list of files where
    that word is found as a value
    """
    with ThreadPoolExecutor(max_workers=len(split_files)) as pool:
        results = pool.map(
            search_keywords_in_files,
            [(files, keywords) for files in split_files],
        )

    return results


def multiprocess_search(split_files: list[list,], keywords: list[str,]):
    """
    Function that provides a multi-process search for keywords in files

    :param split_files: Collection of several lists of text files to search for keywords
    :param keywords: List of keywords to search in files
    :return: Iterator with dictionaries where keyword is a key and a list of files where
    that word is found as a value
    """
    with ProcessPoolExecutor(max_workers=len(split_files)) as pool:
        results = pool.map(
            search_keywords_in_files,
            [(files, keywords) for files in split_files],
        )

    return results


def synchronous_search(split_files: list[list,], keywords: list[str,]) -> list:
    """
    Function that provides synchronous search for keywords in files

    :param split_files: Collection of several lists of text files to search for keywords
    :param keywords: List of keywords to search in files
    :return: List of dictionaries where keyword is a key and a list of files where
    that word is found as a value
    """
    results = []
    for files in split_files:
        args = (files, keywords)
        result = search_keywords_in_files(args)
        results.append(result)
    return results


def main(search_functions: tuple, directory: str = DIRECTORY) -> None:  # type: ignore
    """
    Function to measure the performance of different types of search functions

    :param search_functions: List of functions to search for keywords in specific files
    :param directory: Directory of text files that can be searched by keyword
    """
    files = []
    for file in os.listdir(directory):
        if os.path.splitext(file)[1].lower() in (".txt",):
            files.append(os.path.join(directory, file))
    if not files:
        print("No files provided")
        return
    num_workers = min(8, len(files))
    split_files_among_workers = [files[i::num_workers] for i in range(num_workers)]

    keywords = input("Enter keywords to search for, use a comma as a separator: ")
    if keywords:
        keywords = keywords.split(",")
        keywords = [word.strip() for word in keywords]

        for function in search_functions:
            start_time = time.time()
            results_list = function(split_files_among_workers, keywords)
            end_time = time.time()

            final_results = {keyword: [] for keyword in keywords}
            for result in results_list:
                for keyword in keywords:
                    final_results[keyword].extend(result[keyword])

            print(f"\n{function.__name__} Results:", final_results)
            print("Execution Time:", end_time - start_time, "seconds")

    else:
        print("No keywords are provided")


if __name__ == "__main__":
    search_funcs = (multithreaded_search, multiprocess_search, synchronous_search)
    main(search_funcs)
