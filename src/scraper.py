import requests
import os
from bs4 import BeautifulSoup
import json
from functools import wraps, partial
import csv
import time
from utl import list_from_file
from concurrent.futures import ThreadPoolExecutor

# from utl import extract_value_from_nested
from utl import list_of_dicts_to_csv
from utl import list_to_file
from utl import dict_to_json_file
from utl import filtered_dict_by_value_path_map

from utl import use_session
from utl import retry_decorator
from config import HEADERS, ATTRIBUTES_MAP, URL


@use_session(headers=HEADERS)
def fetch_url(session, url):
    response = session.get(url)
    return response


def soup_url(url):
    response = fetch_url(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


@retry_decorator(max_retries=3, delay=2)
def get_number_of_search_results(url):
    # return number of lots in immoweb DB for a given search url
    soup = soup_url(url)
    number_of_lots = json.loads(soup.find("iw-search")[":result-count"])
    return number_of_lots


@retry_decorator(max_retries=3, delay=2)
# def get_all_lots_from_index_page(url):
def get_all_lots_from_search_page(url):
    # return list (=<30) of dictionaries with basic lot info
    soup = soup_url(url)
    lots = json.loads(soup.find("iw-search")[":results"])
    return lots


@retry_decorator(max_retries=3, delay=3)
def get_full_lot_info(id, url="https://www.immoweb.be/en/classified/"):
    # return huge nested dict (from json) with all lot info
    soup = soup_url(f"{url}{id}")
    full_lot_info = json.loads(
        soup.find("div", "classified")
        .find("script")
        .string.split("window.classified = ")[1][:-10]
    )
    return full_lot_info


def collect_all_ids_from_search_results_page(url):
    # return list of id's (up to 30) from search results page
    lots = get_all_lots_from_search_page(url)
    # lots is  a list of dictionaries
    ids = [filtered_dict_by_value_path_map(lot, ATTRIBUTES_MAP)["id"] for lot in lots]
    return ids


def dump_full_lot_info_to_json_file(id, dump_path="temp/json_dumps"):
    full_info = get_full_lot_info(id)
    if full_info is not None:
        file_path = os.path.join(dump_path, f"{id}.json")
        dict_to_json_file(full_info, file_path)
        # print(f"Info for ID {id} dumped successfully.")
    else:
        print(f"No info retrieved for ID {id}. Skipping.")


def generate_search_urls(start_url):
    # return list pages (page=1,... page=n) for a given search url
    urls = []
    # print(start_url)
    tot_results = get_number_of_search_results(start_url)
    print(tot_results)
    tot_pages = list(range(1, 2 + tot_results // 30))
    urls = [f"{start_url}&page={page}" for page in tot_pages]
    return urls


def collect_all_ids_from_urls(urls):
    ids_new = []

    def collect_ids(url):
        print(url)
        return collect_all_ids_from_search_results_page(url)

    # Использование ThreadPoolExecutor для асинхронного выполнения
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(collect_ids, urls)

        for result in results:
            ids_new.extend(result)

    return ids_new


def dump_all_lots_info_to_json_files(ids, dump_path="temp/json_dumps"):
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Создание задач для каждого id
        futures = [
            executor.submit(dump_full_lot_info_to_json_file, id, dump_path)
            for id in ids
        ]
        # Ожидание завершения всех задач
        for future in futures:
            future.result()  # Этот вызов блокируется, пока задача не будет выполнена


def get_filtered_info_from_json_file(f, dump_path="temp/json_dumps"):
    # file_path = os.path.join(dump_path, f"{id}.json")
    file_path = os.path.join(dump_path, f)
    with open(file_path, "r") as file:
        full_info = json.load(file)
        filtered_info = filtered_dict_by_value_path_map(full_info, ATTRIBUTES_MAP)
    return filtered_info


def extract_filtered_info_from_all_files(dump_path="temp/json_dumps"):
    list_of_json_files = os.listdir(dump_path)
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(
            # get_filtered_info_from_json_file, list_of_json_files[:1000]
            get_filtered_info_from_json_file,
            list_of_json_files,
        )
        return list(results)


def get_all_ids_in_dir(dump_path="temp/json_dumps"):
    list_of_json_files = os.listdir(dump_path)
    return [f.split(".")[0] for f in list_of_json_files]


def get_all_new_ids(start_url=URL):
    # if start_url is None:
    #     start_url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false"
    old_ids = get_all_ids_in_dir()
    urls = generate_search_urls(start_url)
    new_ids = collect_all_ids_from_urls(urls)
    only_new = list(set(new_ids) - set(old_ids))
    return only_new


def collect_ids_from_json_with_cluster(dump_path="temp/json_dumps"):
    cl_ids = []
    for f in os.listdir(dump_path):
        try:
            with open(os.path.join(dump_path, f), "r") as f:
                data = json.load(f)
                # if "cluster" in data:
                if data.get("cluster") and data["cluster"] is not None:
                    print(f"{f} has cluster")
                    print(len(cl_ids))
                    # print(data["cluster"]["units"])
                    cl_ids.extend(
                        [
                            item["id"]
                            for unit in data["cluster"]["units"]
                            for item in unit["items"]
                        ]
                    )
        except Exception as e:
            print(f"{f}: {e}")
    print(len(cl_ids))
    return cl_ids


def get_filtered_info_from_lot_page(id):
    full_info = get_full_lot_info(id)
    if full_info is not None:
        filtered_info = filtered_dict_by_value_path_map(full_info, ATTRIBUTES_MAP)
        return filtered_info
    else:
        print(f"No info retrieved for ID {id}. Skipping.")


# get full filtered_info from all ids
def get_filtered_info_from_ids_list(ids):
    info = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(
            # filtered_dict_by_value_path_map(get_full_lot_info(id), ATTRIBUTES_MAP),
            get_filtered_info_from_lot_page,
            ids
            # get_filtered_info_from_json_file, ids
        )
        for r in results:
            info.append(r)

    return info


if __name__ == "__main__":
    start_url = URL
    urls = generate_search_urls(start_url)
    # print(len(urls))
    ids = collect_all_ids_from_urls(urls[:3])
    # ids = collect_all_ids_from_urls(urls)
    ids = list(set(ids))
    # print(ids[:10])
    print(len(ids))

    filtered_info = get_filtered_info_from_ids_list(ids[:10])
    # print(filtered_info[2])
    list_of_dicts_to_csv(filtered_info, "../data/raw/raw_immoweb_data.csv")
