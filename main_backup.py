import pandas as pd
import networkx as nx

# Membaca dataset jaringan jalan Surabaya
df = pd.read_csv("Surabaya_Edgelist.csv")

# Memeriksa struktur dan isi dataset
print("Lima data pertama:")
print(df.head())

print("\nJumlah baris data:", len(df))
print("Jumlah data kosong:")
print(df.isnull().sum())

# Membuat graf tak berarah
G = nx.Graph()

for _, row in df.iterrows():
	u = int(row["START_NODE"])
	v = int(row["END_NODE"])
	length = float(row["LENGTH"])

	if u != v and length > 0:
		if G.has_edge(u, v):
			# Jika koneksi ganda, simpan panjang terkecil
			if length < G[u][v]["weight"]:
				G[u][v]["weight"] = length
		else:
			G.add_edge(u, v, weight=length)

print("\nJumlah titik:", G.number_of_nodes())
print("Jumlah koneksi unik:", G.number_of_edges())
print("Jumlah komponen terhubung:",
	  nx.number_connected_components(G))

# Mencari komponen terhubung terbesar
komponen_terbesar = max(nx.connected_components(G), key=len)
G_besar = G.subgraph(komponen_terbesar).copy()

print("\nJumlah titik pada komponen terbesar:",
	  G_besar.number_of_nodes())
print("Jumlah koneksi pada komponen terbesar:",
	  G_besar.number_of_edges())

# Memilih 15 titik yang benar-benar terhubung
jumlah_titik = 15

# Ambil titik awal dari komponen terbesar
titik_awal = next(iter(komponen_terbesar))

# Telusuri jaringan menggunakan Breadth-First Search (BFS)
urutan_titik = list(
    nx.bfs_tree(G_besar, source=titik_awal).nodes()
)

# Pilih 15 titik pertama dari hasil penelusuran
titik_pilihan = urutan_titik[:jumlah_titik]

# Bentuk subgraf dari titik-titik pilihan
G_15 = G_besar.subgraph(titik_pilihan).copy()

# Periksa hasilnya
print("\n=== PEMERIKSAAN 15 TITIK ===")
print("Daftar titik:", sorted(G_15.nodes()))
print("Jumlah titik:", G_15.number_of_nodes())
print("Jumlah koneksi:", G_15.number_of_edges())
print("Apakah graf terhubung:", nx.is_connected(G_15))

# ==========================================
# TAHAP 4: MINIMUM SPANNING TREE - KRUSKAL
# ==========================================

# Urutkan semua koneksi berdasarkan panjang jalan
daftar_koneksi = sorted(
    G_15.edges(data=True),
    key=lambda edge: edge[2]["weight"]
)

# Inisialisasi struktur untuk mendeteksi siklus
parent = {node: node for node in G_15.nodes()}
rank = {node: 0 for node in G_15.nodes()}


def cari_akar(node):
    if parent[node] != node:
        parent[node] = cari_akar(parent[node])
    return parent[node]


def gabungkan(u, v):
    akar_u = cari_akar(u)
    akar_v = cari_akar(v)

    if akar_u == akar_v:
        return False

    if rank[akar_u] < rank[akar_v]:
        parent[akar_u] = akar_v
    elif rank[akar_u] > rank[akar_v]:
        parent[akar_v] = akar_u
    else:
        parent[akar_v] = akar_u
        rank[akar_u] += 1

    return True


# Proses pemilihan koneksi menggunakan Kruskal
mst_edges = []
total_panjang = 0

print("\n=== HASIL ALGORITMA KRUSKAL ===")
print("Urutan | Titik Awal - Titik Akhir | Panjang (m)")
print("-" * 55)

for u, v, data in daftar_koneksi:
    panjang = data["weight"]

    if gabungkan(u, v):
        mst_edges.append((u, v, panjang))
        total_panjang += panjang

        print(
            f"{len(mst_edges):6} | "
            f"{u:5} - {v:<5} | "
            f"{panjang:12.2f}"
        )

    if len(mst_edges) == G_15.number_of_nodes() - 1:
        break


# Bentuk graf MST
MST = nx.Graph()
MST.add_nodes_from(G_15.nodes())

for u, v, panjang in mst_edges:
    MST.add_edge(u, v, weight=panjang)

# Validasi hasil
print("\n=== VALIDASI MST ===")
print("Jumlah titik:", MST.number_of_nodes())
print("Jumlah koneksi MST:", MST.number_of_edges())
print("Total panjang jaringan:", round(total_panjang, 2), "meter")
print("Graf terhubung:", nx.is_connected(MST))
print("Tidak mengandung siklus:", nx.is_forest(MST))
print(
    "Jumlah koneksi sesuai:",
    MST.number_of_edges() == G_15.number_of_nodes() - 1
)
print(
    "Total bobot sesuai:",
    abs(
        total_panjang
        - sum(data["weight"] for _, _, data in MST.edges(data=True))
    ) < 1e-6
)
