import asyncio
import aiohttp
from collections import defaultdict
import matplotlib.pyplot as plt

NUM_REQUESTS = 10000
CONCURRENT_REQUESTS = 100
URL = "http://localhost:5000/home"

counts = defaultdict(int)

async def fetch(session, rid):
    try:
        async with session.get(f"{URL}?id={rid}", timeout=5) as resp:
            data = await resp.json()
            msg = data.get("message", "")
            if "Server" in msg:
                sid = msg.split("Server:")[-1].strip()
                counts[sid] += 1
    except Exception:
        print(f"[ERROR] Request {rid} failed")

async def run_all():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(NUM_REQUESTS):
            tasks.append(fetch(session, i))
            if len(tasks) >= CONCURRENT_REQUESTS:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run_all())

    print("\n--- Request Count per Server ---")
    for sid, count in counts.items():
        print(f"Server {sid}: {count}")

    # Plotting
    servers = list(counts.keys())
    values = list(counts.values())
    plt.bar(servers, values, color='skyblue')
    plt.title(f"Task 4-A1: Load Distribution Across Servers ({NUM_REQUESTS} Requests)")
    plt.xlabel("Server ID")
    plt.ylabel("Number of Requests Handled")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("task4-a1-load-distribution.png")
    plt.show()
