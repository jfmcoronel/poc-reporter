import sys
import subprocess
import asyncio
import websockets
import time

PORT = 29830


async def report(ws, path):
    print(path)

    while True:
        time.sleep(1)
        print("Sending...")
        result = subprocess.check_output("date +'%s'", shell=True)
        await ws.send(result)


def reporter_main():
    server = websockets.serve(report, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(server)
    print(f"Listening on port {PORT}...")
    asyncio.get_event_loop().run_forever()


async def inquire(ip):
    uri = f"ws://{ip}:{PORT}"
    async with websockets.connect(uri) as ws:
        while True:
            result = await ws.recv()
            print(ip, result)


def aggregator_main():
    # TODO: Loop queries
    # TODO: Update UI

    ips = [
        "127.0.0.1",
    ]

    for ip in ips:
        asyncio.get_event_loop().run_until_complete(inquire(ip))


def main():
    if len(sys.argv) != 2:
        print("Expects a single argument")
        exit(-1)

    param = sys.argv[1]

    if param == "reporter":
        reporter_main()
    elif param == "aggregator":
        aggregator_main()
    else:
        print("Expects either 'reporter' or 'aggregator' as argument")

if __name__ == "__main__":
    main()
