import requests
import threading
import json
import argparse

def get_product(id, responses, lock, semaphore=None):
    url = f"https://dummyjson.com/products/{id}"
    if semaphore:
        with semaphore:
            print(f'Requesting id {id}')
            response = requests.get(url)
    else:
        print(f'Requesting id {id}')
        response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        with lock:
            responses[id] = data
    else:
        print(f"failed to fetch product #{id}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="usage: python main.py -s -n 10")
    parser.add_argument("-s", action="store_true", help="Flag to indicate whether to use semaphore")
    parser.add_argument("-n", type=int, default=10, help="Number of semaphore")
    return parser.parse_args()


def main():
    args = parse_arguments()
    responses = {}
    lock = threading.Lock()
    semaphore = None
    if args.s:
        semaphore = threading.Semaphore(args.n)

    threads = [threading.Thread(target=get_product, args=(i, responses, lock, semaphore)) for i in range(1, 101)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with open("response.json", "w") as f:
        json.dump(responses, f)


if __name__ == "__main__":
    main()
