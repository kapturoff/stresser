import concurrent.futures
import requests
import time
from collections import namedtuple
from argparse import ArgumentParser

RequestDetails = namedtuple("RequestDetails", "duration")

parser = ArgumentParser()
parser.add_argument(
    "--address", "-a", type=str, required=True, help="address of target"
)
parser.add_argument(
    "--threads", "-t", type=int, required=True, help="count of threads to spam"
)
parser.add_argument(
    "--duration",
    "-d",
    type=int,
    default=10,
    help="duration of running the script (in seconds)",
)
config = vars(parser.parse_args())
start = time.time()


def spam(address: str, finish_time: float) -> int:
    requests_details = []

    while time.time() < finish_time:
        request_start = time.time_ns()
        requests.get(address)
        request_end = time.time_ns()

        # Since time.time_ns() returns nanoseconds, which is 1/1,000,000 of millisecond,
        # it need to divide result to 1,000,000
        requests_details.append(RequestDetails((request_end - request_start) / 1000000))

    return requests_details


with concurrent.futures.ThreadPoolExecutor(max_workers=config["threads"]) as executor:
    address, threads, duration = config.values()
    total_requests_sent = 0
    averages_request_times = []

    print(f"Starting spamming to {address}")

    # Start tasks
    futures = [executor.submit(spam, address, start + duration) for _ in range(threads)]

    # When the tasks are completed
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        total_requests_sent += len(result)  # How many request a thread sent

        # Getting the average speed from all requests made by the thread
        averages_request_times.append(
            sum(map(lambda request_detail: request_detail.duration, result))
            / len(result)
        )

    average_all_threads_speed = round(total_requests_sent / duration)
    average_single_request_speed = sum(averages_request_times) / len(
        averages_request_times
    )

    print(f"Finished! {total_requests_sent} requests sent in {duration} seconds.")
    print(f"Average speed was {average_all_threads_speed} requests per second.")
    print(
        f"Every thread was spending around {average_single_request_speed} ms for request."
    )
