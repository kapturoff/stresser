import concurrent.futures
import requests
import time
from collections import namedtuple
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--address', '-a', type=str, required=True)
parser.add_argument('--threads', '-t', type=int, required=True)
parser.add_argument('--duration', '-d', type=int, default=10)
config = vars(parser.parse_args())
start = time.time()
RequestDetails = namedtuple('RequestDetails', 'duration')

def spam(address: str, finish_time: float) -> int:
     requests_details = []
     
     while time.time() < finish_time:
         request_start = time.time_ns()
         requests.get(address)
         request_end = time.time_ns()

         requests_details.append(RequestDetails((request_end - request_start) / 1000000))
         
     return requests_details

with concurrent.futures.ThreadPoolExecutor(max_workers=config['threads']) as executor:
    address, threads, duration = config.values()
    total_requests_sent = 0
    averages_request_times = []

    print(f'Starting spamming to {address}')

    futures = [executor.submit(spam, address, start + duration) for _ in range(threads)]
    
    for future in concurrent.futures.as_completed(futures):
         result = future.result()
         total_requests_sent += len(result)
         averages_request_times.append(
              sum(map(
                  lambda request_detail: request_detail.duration, 
                  result
              )) / len(result)
         )
    
    print(f'Finished! {total_requests_sent} requests sent in {duration} seconds.')
    print(f'Average speed was {round(total_requests_sent / duration)} requests per second.')
    print(f'Every thread was spending around {sum(averages_request_times) / len(averages_request_times)} ms for request.')
