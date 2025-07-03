import asyncio
import aiohttp
from collections import defaultdict
import matplotlib.pyplot as plt
import time

URL = "http://localhost:5000/home"
NUM_REQUESTS = 10000
CONCURRENT = 100
server_counts = list(range(2, 7))  # N = 2 to 6
results = {}

async def fetch(session, rid):
    try:
        async with session.get(f"{URL}?id={rid}", timeout=5) as resp:
            data = await resp.json()
            msg = data.get("message", "")
            if "Server" in msg:
                sid = msg.split("Server:")[-1].strip()
                return sid
    except Exception:
        return None

async def test_distribution(n_servers):
    # Assume you've already added servers manually beforehand via POST /add
    print(f"Testing with {n_servers} servers...")
    counts = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(NUM_REQUESTS):
            tasks.append(fetch(session, i))
            if len(tasks) >= CONCURRENT:
                results_batch = await asyncio.gather(*tasks)
                for sid in results_batch:
                    if sid:
                        counts[sid] += 1
                tasks = []
        if tasks:
            results_batch = await asyncio.gather(*tasks)
            for sid in results_batch:
                if sid:
                    counts[sid] += 1

    total_handled = sum(counts.values())
    avg = total_handled / n_servers
    print(f"Avg per server with {n_servers}: {avg:.2f}")
    return avg

if __name__ == "__main__":
    print("Starting Task 4-A2 test...")
    for n in server_counts:
        input(f"\n▶️ Please make sure {n} servers are running in Docker. Then press ENTER to continue...")
        avg = asyncio.run(test_distribution(n))
        results[n] = avg
        time.sleep(2)

    # Plot results
    plt.plot(list(results.keys()), list(results.values()), marker='o', color='steelblue')
    plt.title("Task 4-A2: Server Count vs Avg Requests per Server")
    plt.xlabel("Number of Servers")
    plt.ylabel("Avg Requests per Server")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("task4-a2-scaling.png")
    plt.show()
