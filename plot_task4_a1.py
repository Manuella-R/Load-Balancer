import matplotlib.pyplot as plt

# Hardcoded request count results from your last run
server_ids = ["Server 1", "Server 2", "Server 3"]
request_counts = [8003, 997, 1000]

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(server_ids, request_counts, color=['skyblue', 'lightgreen', 'salmon'])
plt.title("Task 4-A1: Load Distribution (10,000 Requests)")
plt.xlabel("Server")
plt.ylabel("Number of Requests")
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Annotate values
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 50, yval, ha='center', fontsize=10)

plt.tight_layout()
plt.savefig("task4-a1-distribution.png")
plt.show()
