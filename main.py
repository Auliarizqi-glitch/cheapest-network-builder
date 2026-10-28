from streamlit_agraph import agraph, Node, Edge, Config
from pathlib import Path
import pandas as pd
import networkx as nx
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Cheapest Network Builder",
    page_icon="🔌",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp {
    background: radial-gradient(ellipse at 10% 0%, #172b48 0%, transparent 38%), #080d18;
    color: #eaf1ff;
    font-family: Inter, sans-serif;
}
[data-testid="stHeader"] {background: rgba(8,13,24,.8)}
[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #263650;
}
[data-testid="stSidebar"] * {color: #eaf1ff}
h1, h2, h3, p, label {color: #eaf1ff}
h1 {font-weight: 800; letter-spacing: -1px}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #142139, #0e1727);
    border: 1px solid #293a55;
    border-radius: 16px;
    padding: 17px;
    min-height: 115px;
}
[data-testid="stMetricLabel"] {color: #98acc9 !important}
[data-testid="stMetricValue"] {
    color: #f4f7ff !important;
    font-weight: 800 !important;
}
.hero {
    padding: 26px 28px;
    border: 1px solid #2a4162;
    border-radius: 22px;
    background: linear-gradient(115deg, #172e4d, #101a2c 65%, #291b32);
    margin-bottom: 22px;
}
.eyebrow {
    color: #72bcff;
    font-size: .75rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.sub {color: #b4c4dc; line-height: 1.6}
.card {
    background: #0e1727;
    border: 1px solid #2a3a53;
    border-radius: 14px;
    padding: 16px;
}
.small {color: #98acc9; font-size: .82rem}
.value {color: #f4f7ff; font-size: 1.15rem; font-weight: 800}
.stButton>button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 43px;
    border: 1px solid #314867;
}
.stButton>button[kind="primary"] {
    background: linear-gradient(90deg, #1675d1, #345eea);
    color: white;
    border: 0;
}
hr {border-color: #293a55}


/* Perbaikan warna tulisan */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
  color: #f1f5f9 !important;
}

.stButton > button {
  color: #ffffff !important;
  background-color: #1b2b43;
  border: 1px solid #49617f;
}

.stButton > button[kind="primary"] {
  color: #ffffff !important;
  background: linear-gradient(90deg, #1675d1, #345eea);
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
  color: #f1f5f9 !important;
}


</style>

<div class="hero">
    <div class="eyebrow">GRAPH OPTIMIZATION · KRUSKAL ALGORITHM</div>
    <h1 style="margin:8px 0 10px">🔌 Cheapest Network Builder</h1>
    <p class="sub">
        Bangun jaringan dengan total panjang minimum.
        Ubah bobot koneksi, amati perubahan Minimum Spanning Tree (MST),
        dan bandingkan estimasi biaya.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 1. PENGATURAN DATA
# =====================================================

FILE_DATA = Path(__file__).parent / "Surabaya_Edgelist.csv"
JUMLAH_NODE = 15


@st.cache_data
def baca_data(path):
    data = pd.read_csv(path)

    required = {"START_NODE", "END_NODE", "LENGTH"}

    if not required.issubset(data.columns):
        raise ValueError(
            "Dataset harus memiliki kolom START_NODE, END_NODE, dan LENGTH."
        )

    data = data[
        ["START_NODE", "END_NODE", "LENGTH"]
    ].dropna().copy()

    data["START_NODE"] = data["START_NODE"].astype(str).str.strip()
    data["END_NODE"] = data["END_NODE"].astype(str).str.strip()
    data["LENGTH"] = pd.to_numeric(
        data["LENGTH"], errors="coerce"
    )

    data = data.dropna(subset=["LENGTH"])

    return data[
        (data["START_NODE"] != data["END_NODE"])
        & (data["LENGTH"] > 0)
    ]


def siapkan_graf(data):
    graf = nx.Graph()

    for baris in data.itertuples(index=False):
        u = baris.START_NODE
        v = baris.END_NODE
        w = float(baris.LENGTH)

        if not graf.has_edge(u, v) or w < graf[u][v]["weight"]:
            graf.add_edge(u, v, weight=w)

    return graf


def pilih_subgraf(graf, n=15, n_awal=100):
    komponen = max(
        nx.connected_components(graf),
        key=len
    )

    graf = graf.subgraph(komponen).copy()

    kandidat = sorted(
        graf.nodes(),
        key=lambda x: (-graf.degree(x), x)
    )[:n_awal]

    terbaik = None
    skor_terbaik = -1

    for awal in kandidat:
        dipilih = {awal}

        while len(dipilih) < n:
            frontier = {
                v
                for u in dipilih
                for v in graf.neighbors(u)
            } - dipilih

            if not frontier:
                break

            def skor(v):
                tetangga_dipilih = sum(
                    x in dipilih for x in graf.neighbors(v)
                )
                return (
                    tetangga_dipilih,
                    graf.degree(v),
                    v
                )

            dipilih.add(max(frontier, key=skor))

        if len(dipilih) != n:
            continue

        subgraf = graf.subgraph(dipilih).copy()

        siklus = (
            subgraf.number_of_edges()
            - subgraf.number_of_nodes()
            + 1
        )

        if nx.is_connected(subgraf) and siklus > skor_terbaik:
            terbaik = subgraf
            skor_terbaik = siklus

    if terbaik is None:
        raise ValueError("Gagal memilih subgraf terhubung.")

    return terbaik


def key_edge(u, v):
    return tuple(sorted((str(u), str(v))))


# =====================================================
# 2. ALGORITMA KRUSKAL
# =====================================================

def kruskal(graf):
    parent = {u: u for u in graf.nodes()}
    rank = {u: 0 for u in graf.nodes()}

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        a = find(u)
        b = find(v)

        if a == b:
            return False

        if rank[a] < rank[b]:
            parent[a] = b
        elif rank[a] > rank[b]:
            parent[b] = a
        else:
            parent[b] = a
            rank[a] += 1

        return True

    edges = sorted(
        graf.edges(data=True),
        key=lambda e: (
            e[2]["weight"],
            min(str(e[0]), str(e[1])),
            max(str(e[0]), str(e[1]))
        )
    )

    mst = nx.Graph()
    mst.add_nodes_from(graf.nodes())

    for u, v, data in edges:
        if union(u, v):
            mst.add_edge(
                u, v,
                weight=float(data["weight"])
            )

            if mst.number_of_edges() == graf.number_of_nodes() - 1:
                break

    return mst


def total(graf):
    return sum(
        float(data["weight"])
        for _, _, data in graf.edges(data=True)
    )


def rupiah(nilai):
    return "Rp" + f"{nilai:,.0f}".replace(",", ".")


# =====================================================
# 3. MEMBACA DATA DAN MENYIAPKAN JARINGAN
# =====================================================

if not FILE_DATA.exists():
    st.error(
        "File Surabaya_Edgelist.csv harus berada satu folder dengan main.py."
    )
    st.stop()

try:
    data = baca_data(str(FILE_DATA))
    g_full = siapkan_graf(data)
    g0 = pilih_subgraf(g_full, JUMLAH_NODE)

except Exception as error:
    st.error(f"Data gagal diproses: {error}")
    st.stop()


# Bobot awal setiap koneksi
initial = {
    key_edge(u, v): float(attr["weight"])
    for u, v, attr in g0.edges(data=True)
}

# Simpan bobot hasil perubahan selama aplikasi berjalan
if (
    "bobot_aktif" not in st.session_state
    or set(st.session_state["bobot_aktif"]) != set(initial)
):
    st.session_state["bobot_aktif"] = initial.copy()


# Membentuk graf dengan bobot terbaru
g = g0.copy()

for u, v in g.edges():
    k = key_edge(u, v)
    g[u][v]["weight"] = float(
        st.session_state["bobot_aktif"][k]
    )


# MST awal dan MST terbaru
mst0 = kruskal(g0)
mst = kruskal(g)


# =====================================================
# 4. SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")

    tariff = st.number_input(
        "Tarif simulasi per meter (Rp)",
        min_value=0,
        value=50000,
        step=5000
    )

    st.caption(
        "Tarif merupakan asumsi simulasi, bukan harga aktual."
    )

    if st.button(
        "↺ Reset semua bobot",
        use_container_width=True
    ):
        st.session_state["bobot_aktif"] = initial.copy()

        for k in list(st.session_state.keys()):
            if str(k).startswith("panjang_"):
                del st.session_state[k]

        st.rerun()

    st.divider()
    st.markdown("### 📊 Dataset")

    st.metric("Baris data", f"{len(data):,}")
    st.metric("Simpul graf lengkap", f"{g_full.number_of_nodes():,}")
    st.metric("Koneksi unik", f"{g_full.number_of_edges():,}")


# =====================================================
# 5. RINGKASAN JARINGAN
# =====================================================

length0 = total(mst0)
length = total(mst)

cost0 = length0 * tariff
cost = length * tariff

st.markdown("### OVERVIEW")
st.header("Ringkasan Jaringan")

a, b, c, d = st.columns(4)

a.metric("Simpul", g.number_of_nodes())
b.metric("Koneksi Kandidat", g.number_of_edges())
c.metric("Koneksi dalam MST", mst.number_of_edges())

d.metric(
    "Total Panjang MST",
    f"{length:,.2f} m",
    delta=(
        f"{length - length0:+,.2f} m"
        if abs(length - length0) > 1e-8
        else "Tidak berubah"
    )
)

e, f = st.columns(2)

e.metric("Estimasi Biaya Saat Ini", rupiah(cost))

f.metric(
    "Perubahan Biaya",
    rupiah(cost - cost0),
    delta_color="inverse"
)

st.caption(
    f"Bobot MST awal: {length0:,.2f} m · "
    "Estimasi biaya = total panjang MST × tarif simulasi."
)




# =====================================================
# 6. VISUALISASI INTERAKTIF + ANIMASI KRUSKAL
# =====================================================

st.markdown("### LIVE TOPOLOGY")
st.header("Visualisasi dan Simulasi Kruskal")

st.caption(
    "Geser simpul dengan mouse. Jalankan simulasi untuk melihat "
    "algoritma Kruskal memeriksa koneksi satu per satu."
)

# Urutkan koneksi berdasarkan bobot, sama seperti algoritma Kruskal
urutan_koneksi = sorted(
    g.edges(data=True),
    key=lambda e: (
        float(e[2]["weight"]),
        min(str(e[0]), str(e[1])),
        max(str(e[0]), str(e[1]))
    )
)

# Buat catatan setiap langkah Kruskal
parent_anim = {n: n for n in g.nodes()}
rank_anim = {n: 0 for n in g.nodes()}

def find_anim(n):
    if parent_anim[n] != n:
        parent_anim[n] = find_anim(parent_anim[n])
    return parent_anim[n]

def union_anim(a, b):
    ra, rb = find_anim(a), find_anim(b)

    if ra == rb:
        return False

    if rank_anim[ra] < rank_anim[rb]:
        parent_anim[ra] = rb
    elif rank_anim[ra] > rank_anim[rb]:
        parent_anim[rb] = ra
    else:
        parent_anim[rb] = ra
        rank_anim[ra] += 1

    return True

langkah_anim = []
diterima_anim = []

for u, v, attr in urutan_koneksi:
    diterima = union_anim(u, v)

    if diterima:
        diterima_anim.append(key_edge(u, v))

    langkah_anim.append({
        "u": u,
        "v": v,
        "weight": float(attr["weight"]),
        "accepted": diterima,
        "selected": diterima_anim.copy()
    })

    if len(diterima_anim) == g.number_of_nodes() - 1:
        break

# Status pemutar animasi
if "kruskal_step" not in st.session_state:
    st.session_state["kruskal_step"] = 0

if "kruskal_playing" not in st.session_state:
    st.session_state["kruskal_playing"] = False

jumlah_langkah = len(langkah_anim)
st.session_state["kruskal_step"] = min(
    max(0, st.session_state["kruskal_step"]),
    max(0, jumlah_langkah - 1)
)

# Kontrol simulasi
p1, p2, p3, p4, p5 = st.columns(5)

with p1:
    if st.button("▶ Jalankan", use_container_width=True):
        st.session_state["kruskal_playing"] = True

with p2:
    if st.button("⏸ Jeda", use_container_width=True):
        st.session_state["kruskal_playing"] = False

with p3:
    if st.button("⏮ Sebelumnya", use_container_width=True):
        st.session_state["kruskal_playing"] = False
        st.session_state["kruskal_step"] = max(
            0, st.session_state["kruskal_step"] - 1
        )

with p4:
    if st.button("⏭ Berikutnya", use_container_width=True):
        st.session_state["kruskal_playing"] = False
        st.session_state["kruskal_step"] = min(
            jumlah_langkah - 1,
            st.session_state["kruskal_step"] + 1
        )

with p5:
    if st.button("↺ Reset", use_container_width=True):
        st.session_state["kruskal_playing"] = False
        st.session_state["kruskal_step"] = 0

# Fragment menjalankan animasi otomatis setiap 1 detik saat diputar
@st.fragment(
    run_every=1.0 if st.session_state["kruskal_playing"] else None
)
def tampilkan_simulasi():
    idx = st.session_state["kruskal_step"]
    langkah = langkah_anim[idx]

    if st.session_state["kruskal_playing"]:
        if idx < jumlah_langkah - 1:
            st.session_state["kruskal_step"] = idx + 1
        else:
            st.session_state["kruskal_playing"] = False

    # Langkah yang ditampilkan
    idx = st.session_state["kruskal_step"]
    langkah = langkah_anim[idx]

    st.progress((idx + 1) / jumlah_langkah)
    st.caption(f"Langkah {idx + 1} dari {jumlah_langkah}")

    u, v = langkah["u"], langkah["v"]

    if langkah["accepted"]:
        st.success(
            f"Koneksi {u} — {v} ({langkah['weight']:.2f} m) "
            "DITERIMA: tidak membentuk siklus."
        )
    else:
        st.warning(
            f"Koneksi {u} — {v} ({langkah['weight']:.2f} m) "
            "DITOLAK: membentuk siklus."
        )

    # Warna koneksi:
    # merah = sudah diterima, kuning = sedang diperiksa,
    # abu-abu = belum dipilih atau ditolak.
    koneksi_diterima = set(langkah["selected"])
    koneksi_sekarang = key_edge(u, v)

    nodes = [
        Node(
            id=str(n),
            label=str(n),
            size=24,
            color="#43a5ff",
            font={"color": "#eaf1ff", "size": 15},
            borderWidth=2
        )
        for n in g.nodes()
    ]

    edges = []

    for a, b, attr in g.edges(data=True):
        k = key_edge(a, b)

        if k == koneksi_sekarang:
            warna = "#fbbf24"
            lebar = 6
        elif k in koneksi_diterima:
            warna = "#ff5263"
            lebar = 4
        else:
            warna = "#52627b"
            lebar = 1

        edges.append(
            Edge(
                source=str(a),
                target=str(b),
                label=f"{attr['weight']:.0f} m",
                color=warna,
                width=lebar,
                title=(
                    f"{a} — {b}: {attr['weight']:.2f} m"
                )
            )
        )

    config = Config(
        width="100%",
        height=560,
        directed=False,
        physics=False,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#ffd166",
        collapsible=False,
        interaction={
            "dragNodes": True,
            "dragView": True,
            "zoomView": True
        }
    )

    agraph(nodes=nodes, edges=edges, config=config)

    st.caption(
        "🟡 Sedang diperiksa · 🔴 Diterima dalam MST · "
        "Abu-abu: koneksi lainnya"
    )

    st.metric(
        "Koneksi diterima sampai langkah ini",
        len(langkah["selected"])
    )

tampilkan_simulasi()




# =====================================================
# 7. MENGUBAH PANJANG KONEKSI
# =====================================================

st.markdown("### INTERACTIVE CONTROLS")
st.header("Ubah Panjang Koneksi")

st.caption(
    "Pilih koneksi, ubah panjangnya, lalu hitung ulang MST. "
    "Warna garis dan ringkasan mengikuti hasil terbaru."
)

edges = sorted(
    g.edges(),
    key=lambda s: (
        min(str(s[0]), str(s[1])),
        max(str(s[0]), str(s[1]))
    )
)


def edge_label(edge):
    u, v = edge
    return (
        f"{u} — {v} "
        f"({g[u][v]['weight']:.2f} m)"
    )


chosen = st.selectbox(
    "Pilih koneksi kandidat",
    edges,
    format_func=edge_label,
    key="pilihan_koneksi"
)

u, v = chosen
k = key_edge(u, v)

current = float(
    st.session_state["bobot_aktif"][k]
)

x1, x2, x3 = st.columns(3)

x1.markdown(
    f'<div class="card">'
    f'<div class="small">Panjang saat ini</div>'
    f'<div class="value">{current:,.2f} m</div>'
    f'</div>',
    unsafe_allow_html=True
)

x2.markdown(
    f'<div class="card">'
    f'<div class="small">Panjang awal</div>'
    f'<div class="value">{initial[k]:,.2f} m</div>'
    f'</div>',
    unsafe_allow_html=True
)

start_mst = k in {
    key_edge(a, b)
    for a, b in mst0.edges()
}

status_awal = (
    "Bagian dari MST awal"
    if start_mst
    else "Bukan bagian dari MST awal"
)

x3.markdown(
    f'<div class="card">'
    f'<div class="small">Status awal</div>'
    f'<div class="value" style="font-size:1rem">'
    f'{status_awal}'
    f'</div></div>',
    unsafe_allow_html=True
)


# Input panjang koneksi
widget_key = f"panjang_{k[0]}_{k[1]}"


if st.session_state.get("_active_edge_key") != k:
    st.session_state[widget_key] = current
    st.session_state["_active_edge_key"] = k
elif widget_key not in st.session_state:
    st.session_state[widget_key] = current


new_weight = st.number_input(
    "Panjang baru (meter)",
    min_value=0.01,
    step=10.0,
    key=widget_key
)

bt1, bt2 = st.columns(2)

with bt1:
    if st.button(
        "⚡ Terapkan & Hitung Ulang MST",
        type="primary",
        use_container_width=True
    ):
        st.session_state["bobot_aktif"][k] = float(new_weight)
        st.rerun()

with bt2:
    if st.button(
        "↺ Reset bobot koneksi ini",
        use_container_width=True
    ):
        st.session_state["bobot_aktif"][k] = initial[k]
        st.session_state[widget_key] = initial[k]
        st.rerun()


# =====================================================
# 8. PERBANDINGAN MST
# =====================================================

st.markdown("### BEFORE VS AFTER")
st.header("Perbandingan MST")

old_edges = {
    key_edge(u, v)
    for u, v in mst0.edges()
}

new_edges = {
    key_edge(u, v)
    for u, v in mst.edges()
}

entering = new_edges - old_edges
leaving = old_edges - new_edges

if entering or leaving:
    st.success(
        "Struktur MST berubah setelah bobot koneksi diperbarui."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🟢 Koneksi masuk")

        for u, v in sorted(entering):
            st.write(
                f"+ **{u} — {v}** · "
                f"{g[u][v]['weight']:.2f} m"
            )

        if not entering:
            st.write("Tidak ada koneksi baru.")

    with c2:
        st.markdown("#### 🔴 Koneksi keluar")

        for u, v in sorted(leaving):
            st.write(
                f"− **{u} — {v}** · "
                f"{g0[u][v]['weight']:.2f} m"
            )

        if not leaving:
            st.write("Tidak ada koneksi yang keluar.")

else:
    st.info(
        "Struktur MST masih sama dengan kondisi awal."
    )

    st.write(
        f"Total panjang MST "
        f"{'berubah' if abs(length-length0) > 1e-8 else 'tetap'}: "
        f"{length0:,.2f} m → {length:,.2f} m."
    )


# Menampilkan koneksi MST yang bobotnya berubah
changed = []

for u, v, attr in mst.edges(data=True):
    k_edge = key_edge(u, v)

    if abs(
        float(st.session_state["bobot_aktif"][k_edge])
        - initial[k_edge]
    ) > 1e-8:
        changed.append({
            "Simpul Awal": u,
            "Simpul Akhir": v,
            "Panjang Awal (m)": initial[k_edge],
            "Panjang Saat Ini (m)": (
                st.session_state["bobot_aktif"][k_edge]
            )
        })

if changed:
    st.markdown("#### Bobot koneksi MST yang berubah")

    st.dataframe(
        pd.DataFrame(changed),
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# 9. DAFTAR KONEKSI MST
# =====================================================

st.markdown("### SELECTED CONNECTIONS")
st.header("Daftar Koneksi pada MST")

rows = []

for u, v, attr in sorted(
    mst.edges(data=True),
    key=lambda e: e[2]["weight"]
):
    w = float(attr["weight"])

    rows.append({
        "Simpul Awal": u,
        "Simpul Akhir": v,
        "Panjang Koneksi (m)": round(w, 2),
        "Estimasi Biaya": rupiah(w * tariff)
    })

st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True,
    hide_index=True
)

q1, q2 = st.columns(2)

q1.metric(
    "Total panjang MST",
    f"{length:,.2f} m"
)

q2.metric(
    "Total estimasi biaya",
    rupiah(cost)
)


# =====================================================
# 10. VALIDASI MST
# =====================================================

with st.expander("✅ Validasi MST"):
    checks = [
        (
            "Graf awal terhubung",
            nx.is_connected(g0)
        ),
        (
            "MST terhubung",
            nx.is_connected(mst)
        ),
        (
            "Jumlah sisi MST = jumlah simpul - 1",
            mst.number_of_edges() == g.number_of_nodes() - 1
        ),
        (
            "MST tidak memiliki siklus",
            nx.is_forest(mst)
        ),
        (
            "Perhitungan total panjang konsisten",
            abs(
                total(mst)
                - sum(
                    float(attr["weight"])
                    for _, _, attr in mst.edges(data=True)
                )
            ) < 1e-6
        )
    ]

    for label, ok in checks:
        if ok:
            st.success(f"✓ {label}")
        else:
            st.error(f"✗ {label}")

    if all(ok for _, ok in checks):
        st.success("Seluruh pemeriksaan MST berhasil.")


# =====================================================
# 11. PENJELASAN ALGORITMA
# =====================================================

with st.expander("ℹ️ Cara Kerja Algoritma Kruskal"):
    st.markdown("""
    1. Semua koneksi diurutkan dari bobot terkecil.
    2. Koneksi diperiksa menggunakan struktur Union-Find.
    3. Koneksi dipilih jika tidak membentuk siklus.
    4. Proses berhenti saat MST memiliki n − 1 sisi.
    5. Jika bobot berubah, MST dihitung ulang berdasarkan bobot terbaru.
    """)


# =====================================================
# 12. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    '<p style="text-align:center;color:#8194b2">'
    'Cheapest Network Builder · Simulasi MST dengan algoritma Kruskal'
    '</p>',
    unsafe_allow_html=True
)