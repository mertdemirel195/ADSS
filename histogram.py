import json
import matplotlib.pyplot as plt

stations = []

# Read JSON line by line
with open("abcTransmissions.json") as f:
    for line in f:
        stations.append(json.loads(line))

freqs = []

# Extract frequency values correctly
for s in stations:
    freq_obj = s.get("frequency")

    if freq_obj and "$numberDecimal" in freq_obj:
        try:
            freqs.append(float(freq_obj["$numberDecimal"]))
        except:
            pass

print("Frequencies found:", len(freqs))

# Plot histogram
plt.hist(freqs, bins=30)
plt.xlabel("Frequency")
plt.ylabel("Number of Stations")
plt.title("Stations per Frequency")

plt.savefig("frequency_histogram.png")

print("Histogram saved")