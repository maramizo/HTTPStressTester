import contextlib
from aiohttp import ClientSession, ClientResponse
import asyncio
from time import perf_counter
import os
import argparse
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
try:
    import uvloop
    uvloop.install()
except ImportError:
    print("uvloop not installed. Using asyncio default event loop.")
    pass

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("url", help="The URL to send requests to")
    arg_parser.add_argument("-a", "--amount", help="The amount of requests to send", type=int, default=10000)
    arg_parser.add_argument("-t", "--time", help="The amount of time to send requests for", type=int, default=10)
    args = arg_parser.parse_args()

    request_url = args.url
    request_amounts = args.amount
    max_time = args.time
    requests_sent = 0
    ok_results = 0
    start_time = perf_counter()

    async def send_request(session: ClientSession):
        async with session.get(request_url) as response:
            global requests_sent
            requests_sent += 1
            if response.status == 200:
                global ok_results
                ok_results += 1
            await response.text()
            print("\033[A                             \033[A")
            now = perf_counter()
            print(f"Sent request {requests_sent}/{request_amounts} ({ok_results} successful) in {now - start_time:.2f}s to {request_url}...")

    async def ddos():
        global start_time
        try:
            async with ClientSession() as session:
                tasks = [asyncio.create_task(send_request(session)) for _ in range(request_amounts)]
                total_time = perf_counter() - start_time
                print(f"Created {len(tasks)} tasks in {total_time:.2f} seconds. Starting tasks...")
                with contextlib.suppress(asyncio.TimeoutError):
                    start_time = perf_counter()
                    await asyncio.wait_for(asyncio.gather(*tasks), max_time)
        except KeyboardInterrupt:
            print("Keyboard interrupt. Exiting...")
        finally:
            print(f"Sent {requests_sent}/{request_amounts} requests, {ok_results} were successful")
            total_time = perf_counter() - start_time
            requests_per_second = requests_sent / total_time
            ms_per_request = total_time / requests_sent * 1000
            print(
                "Time elapsed: {:.2f}, {:.2f} requests per second, {:.2f}ms per request."
                .format(total_time, requests_per_second, ms_per_request)
            )

    asyncio.run(ddos())
