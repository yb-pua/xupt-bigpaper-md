import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.abspath(__file__))
E1 = os.path.join(BASE, "exp1_sm9_bio_kerberos_results")
E2 = os.path.join(BASE, "exp2_sm9_p2pvpn_results")
E3 = os.path.join(BASE, "exp3_sm9_mcp_results")
OUT = os.path.join(BASE, "figures")
os.makedirs(OUT, exist_ok=True)

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)

# fig1: A1 single vs vote5 KRR + BER
s = pd.read_csv(os.path.join(E1, "expA1_summary.csv"), index_col="metric", comment="#")["value"]
fig, ax = plt.subplots(1, 2, figsize=(8, 3.4))
ax[0].bar(["single", "vote5"], [s["single_krr"], s["vote5_krr"]],
          color=["#9ecae1", "#3182bd"], width=0.5)
ax[0].set_ylim(0, 1.05); ax[0].set_ylabel("KRR"); ax[0].set_title("Key Recovery Rate")
for i, v in enumerate([s["single_krr"], s["vote5_krr"]]):
    ax[0].text(i, v + 0.03, f"{v:.3f}", ha="center")
ax[1].bar(["single", "vote5"], [s["single_ber_mean"], s["vote5_ber_mean"]],
          color=["#9ecae1", "#3182bd"], width=0.5)
ax[1].set_ylabel("BER mean (bytes)"); ax[1].set_title("Byte Error Rate")
for i, v in enumerate([s["single_ber_mean"], s["vote5_ber_mean"]]):
    ax[1].text(i, v + 0.5, f"{v:.1f}", ha="center")
fig.suptitle("A1: Majority Voting Improves Key Recovery (single vs 5-vote)")
save(fig, "fig1_A1_vote_gain.png")

# fig2: A2 noise robustness
a2 = pd.read_csv(os.path.join(E1, "expA2_noise_krr.csv"), comment="#")
# krr per noise at max intensity from summary
a2s = pd.read_csv(os.path.join(E1, "expA2_summary.csv"), comment="#")
order = ["brightness", "rotation", "blur", "gaussian", "occlusion"]
labels = ["Brightness", "Rotation", "Blur", "Gaussian", "Occlusion"]
krr = [float(a2s[a2s.noise_type == o].krr_overall.iloc[0]) for o in order]
worst = [float(a2s[a2s.noise_type == o].krr_worst.iloc[0]) for o in order]
x = range(len(order))
fig, ax = plt.subplots(figsize=(6.5, 3.4))
ax.bar(x, krr, width=0.5, color="#3182bd", label="Overall KRR")
ax.scatter(x, worst, color="#de2d26", zorder=5, label="Worst-case KRR")
ax.set_xticks(list(x)); ax.set_xticklabels(labels)
ax.set_ylim(0, 1.05); ax.set_ylabel("KRR"); ax.legend()
ax.set_title("A2: Noise Robustness of Bio-key Recovery (100-person set)")
save(fig, "fig2_A2_noise_krr.png")

# fig3: A4 performance comparison (sign/verify)
a4 = pd.read_csv(os.path.join(E1, "expA4_summary.csv"), comment="#")
sign = a4[(a4.op == "sign")].groupby("algo")["median_ms"].max()
verify = a4[(a4.op == "verify")].groupby("algo")["median_ms"].max()
algos = ["sm9", "sm2", "rsa2048", "ecdsa_p256"]
algo_labels = ["SM9", "SM2", "RSA-2048", "ECDSA-P256"]
fig, ax = plt.subplots(figsize=(6.5, 3.6))
import numpy as np
x = np.arange(len(algos))
w = 0.38
sv = [sign.get(a, 0) for a in algos]
vv = [verify.get(a, 0) for a in algos]
ax.bar(x - w/2, sv, w, label="Sign", color="#3182bd")
ax.bar(x + w/2, vv, w, label="Verify", color="#9ecae1")
ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(algo_labels)
ax.set_ylabel("Median time (ms, log)"); ax.legend()
ax.set_title("A4: SM9 vs SM2 / RSA / ECDSA (pure-Python gmalg)")
save(fig, "fig3_A4_perf.png")

# fig4: B2 scalability (admit p50 + throughput)
b2 = pd.read_csv(os.path.join(E2, "expB2_scalability.csv"), comment="#")
b2o = b2[b2.scheme == "st_ticket_sm9"]
fig, ax = plt.subplots(1, 2, figsize=(8, 3.4))
ax[0].plot(b2o.N, b2o.admit_p50_ms, "o-", color="#3182bd")
ax[0].set_xlabel("N"); ax[0].set_ylabel("Admit p50 (ms)"); ax[0].set_title("Admission latency")
ax[1].plot(b2o.N, b2o.throughput_mbps, "s-", color="#de2d26")
ax[1].set_xlabel("N"); ax[1].set_ylabel("Throughput (Mbps)"); ax[1].set_title("Aggregate throughput")
fig.suptitle("B2: Scalability (N=10/50/100/200)")
save(fig, "fig4_B2_scalability.png")

# fig5: C2 performance ours vs OAuth (log scale)
c2 = pd.read_csv(os.path.join(E3, "expC2_performance.csv"), comment="#")
fig, ax = plt.subplots(1, 2, figsize=(8, 3.4))
conc = [100, 500]
ours = c2[c2.scheme == "ours"]; oauth = c2[c2.scheme == "oauth"]
ax[0].bar([f"{c}" for c in conc], ours.p50_ms / 1000.0, 0.35, label="Ours (s)", color="#3182bd")
ax[0].set_yscale("log"); ax[0].set_ylabel("p50 (log)"); ax[0].set_title("Latency p50")
ax[0].legend()
ax[1].bar([f"{c}" for c in conc], oauth.qps, 0.35, label="OAuth QPS", color="#9ecae1")
ax[1].set_yscale("log"); ax[1].set_ylabel("QPS (log)"); ax[1].set_title("OAuth QPS (baseline)")
ax[1].legend()
fig.suptitle("C2: Trend comparison vs OAuth (GIL-limited, not absolute)")
save(fig, "fig5_C2_perf.png")

# fig6: C3 attack block rate (ours vs oauth vs noauth)
c3 = pd.read_csv(os.path.join(E3, "expC3_attack_matrix.csv"), comment="#")
piv = c3.pivot_table(index="attack_type", columns="scheme", values="block_rate", aggfunc="mean")
piv = piv[["ours", "oauth", "noauth"]].fillna(0)
fig, ax = plt.subplots(figsize=(7, 3.6))
x = np.arange(len(piv)); w = 0.25
ax.bar(x - w, piv["ours"], w, label="Ours", color="#3182bd")
ax.bar(x, piv["oauth"], w, label="OAuth", color="#9ecae1")
ax.bar(x + w, piv["noauth"], w, label="NoAuth", color="#d9d9d9")
ax.set_xticks(x); ax.set_xticklabels(piv.index, rotation=30, ha="right")
ax.set_ylim(0, 1.1); ax.set_ylabel("Block rate"); ax.legend()
ax.set_title("C3: Attack interception (6 attack types)")
save(fig, "fig6_C3_attacks.png")

# fig7: C4 security matrix heatmap
c4 = pd.read_csv(os.path.join(E3, "expC4_security_matrix.csv"), usecols=[0, 1, 2], comment="#")
mat = c4.pivot_table(index="dimension", columns="scheme", values="value", aggfunc="max")
mat = mat[["kerberos_std", "kerberos_sm", "oauth21", "ours"]]
dim_names = {"anti_replay":"Anti-replay","anti_forgery":"Anti-forgery","perm_granularity":"Granularity",
             "caller_binding":"Caller-binding","audit_attribution":"Audit","revocation":"Revocation","guomi":"SM-compliance"}
mat.index = [dim_names.get(i, i) for i in mat.index]
fig, ax = plt.subplots(figsize=(6, 3.6))
im = ax.imshow(mat.values, cmap="Blues", vmin=0, vmax=1, aspect="auto")
ax.set_xticks(range(mat.shape[1])); ax.set_xticklabels(["Kerberos\nstd","SM-Kerb","OAuth2.1","Ours"])
ax.set_yticks(range(mat.shape[0])); ax.set_yticklabels(mat.index)
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        ax.text(j, i, int(mat.values[i, j]), ha="center", va="center",
                color="black" if mat.values[i, j] < 0.5 else "white")
ax.set_title("C4: Security matrix (7 dims x 4 schemes)")
save(fig, "fig7_C4_matrix.png")

# fig8: B3 tunnel shaping (entropy raw vs shaped)
b3 = pd.read_csv(os.path.join(E2, "expB3_tunnel_shaping.csv"), comment="#")
flows = ["period", "request", "burst"]
raw = [float(b3[(b3.flow_type==f)&(b3.scheme=="sm9_raw")].pkt_len_entropy.iloc[0]) for f in flows]
shaped = [float(b3[(b3.flow_type==f)&(b3.scheme=="sm9_shaped")].pkt_len_entropy.iloc[0]) for f in flows]
fig, ax = plt.subplots(figsize=(6.5, 3.4))
x = np.arange(len(flows)); w = 0.35
ax.bar(x - w/2, raw, w, label="Raw", color="#9ecae1")
ax.bar(x + w/2, shaped, w, label="Shaped", color="#3182bd")
ax.set_xticks(x); ax.set_xticklabels(["Period", "Request", "Burst"])
ax.set_ylabel("Packet-length entropy"); ax.legend()
ax.set_title("B3: Traffic shaping entropy gain (burst unchanged)")
save(fig, "fig8_B3_shaping.png")

print("ALL DONE:", sorted(os.listdir(OUT)))
