"""Module for comparing the performance of multi-threaded and multi-process searches using Queues"""

import multiprocessing
import os
import threading
import time
from queue import Queue

from seed import DIRECTORY


def search_keywords_in_files(files: list, keywords: list[str,], result_queue: Queue):
    """
    Function to search for keywords in specific files and add filenames to a common
    queue if a keyword is found in the file

    :param files: List of text files to search for keywords
    :param keywords: List of keywords to search in files
    :return: None, found files are added to the queue that was initialized to the
    level above and passed to the function
    """
    result = {keyword: [] for keyword in keywords}
    for file in files:
        try:
            with open(file, "r", encoding="UTF-8") as fd:
                content = fd.read()
                for keyword in keywords:
                    if keyword.lower() in content.lower():
                        result[keyword].append(file)
        except (
            FileNotFoundError,
            IsADirectoryError,
            PermissionError,
            UnicodeDecodeError,
        ) as err:
            print(f"Error reading file {file}: {err}")
    result_queue.put(result)


def multithreaded_search(split_files: list[list,], keywords: list[str,]):
    """
    Function that provides a multi-threaded search for keywords in files

    :param split_files: Collection of several lists of text files to search for keywords
    :param keywords: List of keywords to search in files
    :return: Dictionary where keyword is a key and a list of files where
    that word is found as a value
    """
    threads = []
    result_queue = Queue()

    for files_wor_worker in split_files:
        thread = threading.Thread(
            target=search_keywords_in_files,
            args=(files_wor_worker, keywords, result_queue),
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result_queue


def multiprocess_search(split_files: list[list,], keywords: list[str,]):
    """
    Function that provides a multi-process search for keywords in files

    :param split_files: Collection of several lists of text files to search for keywords
    :param keywords: List of keywords to search in files
    :return: Dictionary where keyword is a key and a list of files where
    that word is found as a value
    """
    processes = []
    result_queue = multiprocessing.Queue()

    for files_wor_worker in split_files:
        process = multiprocessing.Process(
            target=search_keywords_in_files,
            args=(files_wor_worker, keywords, result_queue),
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return result_queue

def synchronous_search(split_files: list[list,], keywords: list[str,]):
    """
    Function that provides synchronous search for keywords in files

    :param split_files: Collection of several lists of text files to search for keywords
    :param keywords: List of keywords to search in files
    :return: Dictionary where keyword is a key and a list of files where
    that word is found as a value
    """
    result_queue = Queue()

    for files_wor_worker in split_files:
        search_keywords_in_files(files_wor_worker, keywords, result_queue)

    return result_queue


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
            result_queue = function(split_files_among_workers, keywords)
            end_time = time.time()

            final_result = {keyword: [] for keyword in keywords}
            while not result_queue.empty():
                process_result = result_queue.get()
                for keyword, files_found in process_result.items():
                    final_result[keyword].extend(files_found)

            print(f"\n{function.__name__} Results:", final_result)
            print("Execution Time:", end_time - start_time, "seconds")

    else:
        print("No keywords are provided")


if __name__ == "__main__":
    search_funcs = (multithreaded_search, multiprocess_search, synchronous_search)
    main(search_funcs)
