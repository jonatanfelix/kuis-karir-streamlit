import streamlit as st
import random
import plotly.graph_objects as go # Untuk grafik radar
from datetime import datetime # Import di sini

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Kisah Karir Legendaris Anda", page_icon="📜", layout="wide")

# --- Data & Definisi ---

# Atribut Inti Karir (Untuk Grafik Radar & Skor)
daftar_atribut_inti = sorted([
    "Analitis", "Strategis", "Kreatif", "Inovatif", "Kolaboratif",
    "Komunikatif", "Empatik", "Kepemimpinan", "Praktis", "Adaptif",
    "Teliti", "Visioner", "Intuitif", "Berani Ambil Risiko", "Manajerial"
])

# Bakat Terpendam
definisi_bakat_terpendam = {
    "Diplomat_Alami": {
        "nama": "Diplomat Alami", "emoji": "🕊️",
        "deskripsi": "Kemampuan luar biasa untuk menengahi, membangun konsensus, dan menyelesaikan konflik dengan keanggunan.",
        "pemicu_deskripsi": "Pilihanmu secara konsisten menunjukkan keinginan untuk harmoni dan pemahaman bersama."
    },
    "Inovator_Radikal": {
        "nama": "Inovator Radikal", "emoji": "💡",
        "deskripsi": "Pikiran yang tak kenal batas, selalu menantang status quo dan melahirkan ide-ide terobosan.",
        "pemicu_deskripsi": "Keberanianmu untuk memilih solusi non-konvensional sangat menonjol."
    },
    "Benteng_Ketahanan": {
        "nama": "Benteng Ketahanan", "emoji": "🛡️",
        "deskripsi": "Kekuatan mental dan emosional yang luar biasa untuk bangkit dari kegagalan dan menghadapi tekanan.",
        "pemicu_deskripsi": "Pilihanmu menunjukkan kegigihan dan kemampuan untuk tetap tegar di tengah kesulitan."
    },
    "Pendeteksi_Pola_Tersembunyi": {
        "nama": "Pendeteksi Pola Tersembunyi", "emoji": "🔍",
        "deskripsi": "Intuisi tajam dan kemampuan analitis untuk melihat koneksi dan makna yang tak terlihat oleh orang lain.",
        "pemicu_deskripsi": "Kamu kerap memilih untuk menggali lebih dalam dan memahami nuansa."
    }
}

# Pertanyaan, Efek, Artefak (Lencana), dan Pemicu Bakat
daftar_pertanyaan = [
    {
        "id": "q1",
        "tipe": "skenario", # tipe bisa 'skenario', 'dilema', 'refleksi'
        "teks": "Sebuah proyek tim menemui jalan buntu karena perbedaan pendapat yang tajam. Apa tindakan pertamamu sebagai anggota tim?",
        "gambar": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80", # Tim diskusi alot
        "opsi": {
            "A": "Mencari data pendukung untuk argumenku dan menyajikannya secara logis.",
            "B": "Menjadi penengah, mendengarkan semua sisi, dan mencari titik temu.",
            "C": "Mengusulkan ide 'gila' yang benar-benar baru untuk memecah kebuntuan.",
            "D": "Memilih untuk mengerjakan bagianku sendiri dulu sambil menunggu situasi mereda."
        },
        "efek_jawaban": {
            "A": {"atribut": {"Analitis": 2, "Komunikatif": 1}, "artefak": "Artefak Logika Argumen"},
            "B": {"atribut": {"Kolaboratif": 2, "Empatik": 1, "Komunikatif":1}, "artefak": "Artefak Jembatan Harmoni", "pemicu_bakat": {"Diplomat_Alami": 1}},
            "C": {"atribut": {"Kreatif": 2, "Inovatif": 1, "Berani Ambil Risiko":1}, "artefak": "Artefak Ide Pemecah", "pemicu_bakat": {"Inovator_Radikal": 1}},
            "D": {"atribut": {"Praktis": 1, "Adaptif": 1}, "artefak": "Artefak Fokus Mandiri"}
        }
    },
    {
        "id": "q2",
        "tipe": "dilema",
        "teks": "Kamu menemukan cara untuk menyelesaikan proyek besar jauh lebih cepat, tapi membutuhkan pengambilan risiko signifikan yang bisa berdampak pada kualitas jika gagal. Apa keputusanmu?",
        "gambar": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80", # Simpang jalan, risiko
        "opsi": {
            "A": "Tetap pada jalur aman dan teruji, kualitas adalah prioritas utama.",
            "B": "Mengambil risiko tersebut setelah melakukan mitigasi sebaik mungkin.",
            "C": "Mencari cara ketiga: inovasi yang mengurangi risiko namun tetap mempercepat.",
            "D": "Mendiskusikan risiko ini secara transparan dengan atasan/klien sebelum memutuskan."
        },
        "efek_jawaban": {
            "A": {"atribut": {"Teliti": 2, "Praktis": 1}, "artefak": "Artefak Standar Emas"},
            "B": {"atribut": {"Berani Ambil Risiko": 2, "Adaptif": 1, "Strategis":1}, "artefak": "Artefak Lompatan Keberanian", "pemicu_bakat": {"Benteng_Ketahanan": 1, "Inovator_Radikal": 0.5}},
            "C": {"atribut": {"Inovatif": 2, "Kreatif": 1, "Analitis":1}, "artefak": "Artefak Solusi Cerdas"},
            "D": {"atribut": {"Komunikatif": 2, "Kolaboratif": 1}, "artefak": "Artefak Transparansi Proaktif", "pemicu_bakat": {"Diplomat_Alami": 0.5}}
        }
    },
    {
        "id": "q3",
        "tipe": "refleksi",
        "teks": "Pikirkan tentang pekerjaan atau aktivitas yang paling membuatmu lupa waktu (flow state). Elemen apa yang paling dominan dalam pengalaman tersebut?",
        "gambar": "https://images.unsplash.com/photo-1508697018013-fdc3d8759b90?ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80", # Orang fokus kerja
        "opsi": {
            "A": "Memecahkan masalah yang kompleks dan menantang secara intelektual.",
            "B": "Berkolaborasi dan berinteraksi secara intens dengan orang lain untuk tujuan bersama.",
            "C": "Menciptakan sesuatu yang baru, mengekspresikan ide, atau merancang sesuatu yang indah.",
            "D": "Melihat hasil nyata dari pekerjaan, merapikan, atau menyelesaikan tugas secara efisien."
        },
        "efek_jawaban": {
            "A": {"atribut": {"Analitis": 2, "Visioner": 1}, "artefak": "Artefak Kepuasan Intelektual", "pemicu_bakat": {"Pendeteksi_Pola_Tersembunyi": 1}},
            "B": {"atribut": {"Kolaboratif": 2, "Sosial": 1, "Empatik":1}, "artefak": "Artefak Sinergi Tim"}, # 'Sosial' ditambahkan ke daftar_atribut_inti jika belum ada
            "C": {"atribut": {"Kreatif": 2, "Inovatif": 1, "Estetis":1}, "artefak": "Artefak Aliran Kreatif"}, # 'Estetis' ditambahkan
            "D": {"atribut": {"Praktis": 2, "Manajerial": 1, "Teliti":1}, "artefak": "Artefak Produktivitas Nyata"}
        }
    }
    # Tambahkan lebih banyak pertanyaan dengan variasi tipe dan efek
]
# Pastikan semua atribut dari efek_jawaban ada di daftar_atribut_inti
for q in daftar_pertanyaan:
    for opt_data in q['efek_jawaban'].values():
        for attr_key in opt_data['atribut'].keys():
            if attr_key not in daftar_atribut_inti:
                daftar_atribut_inti.append(attr_key)
daftar_atribut_inti = sorted(list(set(daftar_atribut_inti)))


# Persona Inti Karir (Sebelumnya Gelar Karir Legendary)
persona_inti_karir = {
    "Alkemis_Inovasi": {
        "nama_persona": "Alkemis Inovasi", "simbol": "🧪✨",
        "deskripsi": "Kamu mengubah ide mentah menjadi emas terobosan. Dengan perpaduan kreativitas, analisis, dan keberanian bereksperimen, kamu merintis jalur baru dan menciptakan solusi yang tak terpikirkan sebelumnya.",
        "atribut_utama": ["Inovatif", "Kreatif", "Analitis", "Berani Ambil Risiko"],
        "artefak_kunci": ["Artefak Ide Pemecah", "Artefak Solusi Cerdas", "Artefak Lompatan Keberanian"],
        "jalur_potensial": ["Product Developer/Manager", "R&D Specialist", "Entrepreneur Teknologi", "UX Visionary", "Konsultan Inovasi"],
        "saran_pengembangan": "Pertajam kemampuan presentasi untuk 'menjual' ide-ide brilianmu.",
        "misi_oracle": "Identifikasi satu masalah di sekitarmu dan dalam 3 hari ke depan, tuliskan 5 solusi 'gila' untuknya."
    },
    "Arsitek_Harmoni_Tim": {
        "nama_persona": "Arsitek Harmoni Tim", "simbol": "🤝🏛️",
        "deskripsi": "Kamu membangun fondasi tim yang kokoh dan lingkungan kerja yang kolaboratif. Dengan empati, komunikasi yang efektif, dan kemampuan diplomasi, kamu menyatukan individu menjadi kekuatan kolektif yang luar biasa.",
        "atribut_utama": ["Kolaboratif", "Empatik", "Komunikatif", "Kepemimpinan"],
        "artefak_kunci": ["Artefak Jembatan Harmoni", "Artefak Sinergi Tim", "Artefak Transparansi Proaktif"],
        "jalur_potensial": ["Human Resources Manager", "Project Manager (Agile/Scrum)", "Team Lead/Supervisor", "Community Manager", "Mediator Profesional"],
        "saran_pengembangan": "Pelajari teknik fasilitasi untuk memimpin diskusi kelompok yang lebih produktif.",
        "misi_oracle": "Dalam minggu ini, tawarkan bantuan konkret kepada satu rekan kerja yang terlihat membutuhkan."
    },
    "Navigator_Data_Strategis": {
        "nama_persona": "Navigator Data Strategis", "simbol": "🧭📊",
        "deskripsi": "Kamu memetakan lautan informasi, menemukan pola tersembunyi, dan menerjemahkannya menjadi strategi yang cerdas. Dengan ketelitian, logika, dan visi ke depan, kamu memandu keputusan menuju hasil yang optimal.",
        "atribut_utama": ["Analitis", "Strategis", "Teliti", "Visioner"],
        "artefak_kunci": ["Artefak Logika Argumen", "Artefak Standar Emas", "Artefak Kepuasan Intelektual"],
        "jalur_potensial": ["Data Scientist/Analyst", "Business Intelligence Consultant", "Market Researcher", "Financial Planner", "Strategic Planner"],
        "saran_pengembangan": "Kuasai alat visualisasi data untuk menyajikan temuanmu dengan lebih dampak.",
        "misi_oracle": "Pilih satu topik yang menarik minatmu dan habiskan 1 jam untuk menganalisis data terkait yang tersedia online."
    }
    # Tambahkan lebih banyak persona inti
}


# --- Fungsi Helper ---
def reset_kisah():
    st.session_state.tahap_kisah = 0
    st.session_state.atribut_petualang = {attr: 0 for attr in daftar_atribut_inti}
    st.session_state.nama_petualang_kisah = ""
    st.session_state.koleksi_artefak_karir = []
    st.session_state.bakat_terpendam_terbuka = {} # {id_bakat: skor_pemicu}
    st.session_state.jejak_langkah_penting = [] # Menyimpan {id_pertanyaan, pilihan_teks}
    st.session_state.status_kisah = "mulai"

def get_persona_inti_final(skor_atribut, artefak_dimiliki, bakat_terbuka_list):
    skor_persona = {}
    for id_persona, detail_persona in persona_inti_karir.items():
        skor_persona[id_persona] = 0
        # Skor dari atribut utama
        for atribut_k in detail_persona["atribut_utama"]:
            skor_persona[id_persona] += skor_atribut.get(atribut_k, 0) * 2
        # Skor dari artefak kunci
        for artefak_k in detail_persona["artefak_kunci"]:
            if artefak_k in artefak_dimiliki:
                skor_persona[id_persona] += 5
        # Skor bonus jika bakat terpendam relevan (ini bisa jadi lebih kompleks)
        # Misalnya, jika "Inovator_Radikal" terbuka, skor "Alkemis_Inovasi" naik
        if detail_persona["nama_persona"] == "Alkemis Inovasi" and "Inovator Radikal" in bakat_terbuka_list:
            skor_persona[id_persona] += 7
        if detail_persona["nama_persona"] == "Arsitek Harmoni Tim" and "Diplomat Alami" in bakat_terbuka_list:
            skor_persona[id_persona] += 7

    if not any(skor_persona.values()):
        return random.choice(list(persona_inti_karir.values()))
    persona_terpilih_id = max(skor_persona, key=skor_persona.get)
    return persona_inti_karir[persona_terpilih_id]

# --- Inisialisasi State ---
if 'status_kisah' not in st.session_state:
    reset_kisah()

# --- JURNAL PETUALANG (Sidebar) ---
with st.sidebar:
    st.header(f"📜 Jurnal {st.session_state.get('nama_petualang_kisah', 'Petualang')}")

    if st.session_state.status_kisah != "mulai" and st.session_state.status_kisah != "selesai":
        st.caption(f"Bab ke-{st.session_state.tahap_kisah + 1} dari {len(daftar_pertanyaan)}")
    elif st.session_state.status_kisah == "selesai":
        st.caption("Kisah Telah Tertulis!")
    else:
        st.caption("Siap Menulis Takdir?")
    st.markdown("---")

    st.subheader("✨ Aura Karir")
    if any(st.session_state.get('atribut_petualang', {}).values()):
        # Persiapan data untuk grafik radar
        attrs_to_plot = [attr for attr, score in st.session_state.atribut_petualang.items() if score > 0]
        scores_to_plot = [st.session_state.atribut_petualang[attr] for attr in attrs_to_plot]

        if len(attrs_to_plot) >= 3 : # Radar butuh min 3 kategori
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores_to_plot + [scores_to_plot[0]], # Loop back to start for closed shape
                theta=attrs_to_plot + [attrs_to_plot[0]],
                fill='toself',
                name='Skor Atribut'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, max(scores_to_plot) if scores_to_plot else 1])),
                showlegend=False, height=250, margin=dict(l=40, r=40, t=40, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback jika atribut < 3, tampilkan sebagai list saja
            for attr_name, attr_score in sorted(st.session_state.atribut_petualang.items(), key=lambda item: item[1], reverse=True):
                if attr_score > 0:
                    st.markdown(f"- {attr_name}: {attr_score}")

    else:
        st.caption("Aura belum terbentuk...")
    st.markdown("---")


    st.subheader("🛠️ Koleksi Artefak Karir")
    if st.session_state.get('koleksi_artefak_karir'):
        for artefak in st.session_state.koleksi_artefak_karir:
            st.markdown(f"- {artefak}") # Bisa ditambahkan emoji per artefak jika ada mapping
    else:
        st.caption("Belum ada artefak terkumpul.")
    st.markdown("---")

    st.subheader("🔮 Bakat Terpendam Terungkap")
    bakat_terpendam_aktif = []
    if st.session_state.get('bakat_terpendam_terbuka'):
        for bakat_id, skor_pemicu in st.session_state.bakat_terpendam_terbuka.items():
            if skor_pemicu >= 1: # Asumsi skor 1 cukup untuk mengaktifkan
                detail_bakat = definisi_bakat_terpendam[bakat_id]
                st.markdown(f"- {detail_bakat['emoji']} **{detail_bakat['nama']}**")
                bakat_terpendam_aktif.append(detail_bakat['nama'])
    if not bakat_terpendam_aktif:
        st.caption("Masih menjadi misteri...")

    st.markdown("---")
    if st.session_state.status_kisah != "mulai":
        if st.button("Tulis Ulang Kisahmu 🔁", use_container_width=True, key="ulang_jurnal"):
            reset_kisah()
            st.rerun()

# --- AREA UTAMA KISAH ---
if st.session_state.status_kisah == "mulai":
    st.title("📜 Kisah Karir Legendaris Anda: Menempa Takdir Profesional 📜")
    st.markdown("Setiap pilihan adalah goresan pena takdirmu. Jawablah dengan jujur, temukan artefak kekuatanmu, ungkap bakat terpendam, dan raih persona karir legendarismu!")
    st.image("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", caption="Perpustakaan takdir menanti kisahmu...")

    nama_petualang = st.text_input("Ukirlah namamu, wahai Penulis Takdir:", key="nama_input_kisah")
    if st.button("Mulai Menulis Takdir!", type="primary", use_container_width=True):
        if nama_petualang:
            st.session_state.nama_petualang_kisah = nama_petualang
            st.session_state.status_kisah = "berlangsung"
            st.rerun()
        else:
            st.warning("Setiap kisah agung dimulai dengan sebuah nama.")

elif st.session_state.status_kisah == "berlangsung":
    idx_bab = st.session_state.tahap_kisah
    bab_saat_ini = daftar_pertanyaan[idx_bab]

    with st.container(): # Mirip layout di gambar
        st.image(bab_saat_ini["gambar"], use_column_width='auto', caption=f"Ilustrasi Bab ke-{idx_bab+1}")
        st.markdown(f"### Bab ke-{idx_bab+1}: {bab_saat_ini['teks']}")
        st.markdown("---")
        st.markdown("#### Goresan Pilihanmu:")

        for key_pilihan, teks_pilihan in bab_saat_ini["opsi"].items():
            if st.button(teks_pilihan, key=f"btn_bab{idx_bab}_{key_pilihan}", use_container_width=True):
                efek = bab_saat_ini["efek_jawaban"][key_pilihan]
                st.session_state.jejak_langkah_penting.append({"bab": bab_saat_ini["id"], "pilihan": teks_pilihan, "artefak": efek.get("artefak","")})

                # Update Atribut
                for attr, val in efek["atribut"].items():
                    st.session_state.atribut_petualang[attr] = st.session_state.atribut_petualang.get(attr,0) + val

                # Tambah Artefak
                artefak_baru = efek.get("artefak")
                if artefak_baru and artefak_baru not in st.session_state.koleksi_artefak_karir:
                    st.session_state.koleksi_artefak_karir.append(artefak_baru)
                    st.toast(f"Kamu menemukan: {artefak_baru}!", icon="🛠️")

                # Cek Pemicu Bakat Terpendam
                pemicu_bakat_efek = efek.get("pemicu_bakat", {})
                for bakat_id, skor_pemicu_tambah in pemicu_bakat_efek.items():
                    skor_lama = st.session_state.bakat_terpendam_terbuka.get(bakat_id, 0)
                    skor_baru = skor_lama + skor_pemicu_tambah
                    st.session_state.bakat_terpendam_terbuka[bakat_id] = skor_baru
                    # Cek apakah baru saja terbuka (misal, skor lama < 1 dan skor baru >=1)
                    if skor_lama < 1 and skor_baru >=1:
                         st.toast(f"🔮 Bakat Terpendam Terungkap: {definisi_bakat_terpendam[bakat_id]['nama']}!", icon="✨")


                # Lanjut bab atau selesai
                if idx_bab < len(daftar_pertanyaan) - 1:
                    st.session_state.tahap_kisah += 1
                else:
                    st.session_state.status_kisah = "selesai"
                st.rerun()
                break

elif st.session_state.status_kisah == "selesai":
    st.balloons()
    persona_final = get_persona_inti_final(
        st.session_state.atribut_petualang,
        st.session_state.koleksi_artefak_karir,
        bakat_terpendam_aktif # List nama bakat yang aktif dari sidebar
    )

    st.title(f"🗺️ Peta Takdir Karir {st.session_state.nama_petualang_kisah} Telah Tergambar! 🗺️")
    st.markdown(f"<h2 style='text-align: center; color: #FF8C00;'>{persona_final['simbol']} {persona_final['nama_persona']} {persona_final['simbol']}</h2>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("👤 Persona Inti Anda:")
    st.info(persona_final['deskripsi'])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛠️ Rasi Bintang Keahlian (Artefak Utama):")
        # Ambil artefak kunci dari persona, dan cek mana yang dimiliki pengguna
        for artefak_kunci_persona in persona_final["artefak_kunci"]:
            if artefak_kunci_persona in st.session_state.koleksi_artefak_karir:
                st.markdown(f"- ✅ {artefak_kunci_persona} (Dimiliki)")
            else:
                st.markdown(f"- ⚪️ {artefak_kunci_persona} (Potensi Terpendam)")
        if not st.session_state.koleksi_artefak_karir: st.caption("Belum ada artefak terkumpul.")

    with col2:
        st.subheader("💧 Sungai Potensi (Atribut Terkuat):")
        atribut_teratas = sorted(
            [(attr, score) for attr, score in st.session_state.atribut_petualang.items() if score > 0],
            key=lambda x: x[1], reverse=True
        )[:3] # Ambil 3 teratas
        for attr, score in atribut_teratas:
            st.markdown(f"- **{attr}** (Skor: {score})")
        if not atribut_teratas: st.caption("Aliran potensi belum deras.")

    st.markdown("---")
    st.subheader("🌱 Lembah Pengembangan & 🔮 Ramalan Sang Oracle:")
    st.warning(f"**Saran Oracle untuk Pengembangan:** {persona_final['saran_pengembangan']}")

    st.markdown("**Jalur Karir Potensial untuk dijelajahi:**")
    for jalur in persona_final['jalur_potensial']:
        st.markdown(f"- 👉 {jalur}")

    if bakat_terpendam_aktif:
        st.success(f"**Oracle Berbisik:** \"Bakat Terpendammu sebagai **{', '.join(bakat_terpendam_aktif)}** akan menjadi aset tak ternilai. Gunakan dengan bijak!\"")

    st.success(f"**Misi Pertamamu dari Sang Oracle:** {persona_final['misi_oracle']}")

    st.markdown("---")
    st.markdown(f"<p style='text-align:center;'>Ingatlah, {st.session_state.nama_petualang_kisah}, ini adalah peta awal. Takdir sesungguhnya ada di tanganmu untuk terus ditulis dan dijelajahi!</p>", unsafe_allow_html=True)

# --- Footer ---
# Ambil nama pengguna dan tahun saat ini terlebih dahulu
nama_footer = st.session_state.get('nama_petualang_kisah', 'Streamlit Scribe')
tahun_footer = st.session_state.get('current_year', datetime.now().year) # Pastikan datetime diimport jika belum

st.markdown(f"<p style='text-align:center; font-size:small;'>Kisah Karir Legendaris Anda © {nama_footer} {tahun_footer}</p>", unsafe_allow_html=True)

# Set current year once (ini sebaiknya dilakukan di awal script atau saat inisialisasi)
if 'current_year' not in st.session_state:
    from datetime import datetime # Pastikan ini ada di awal file jika belum
    st.session_state.current_year = datetime.now().year
    # st.rerun() # Hati-hati dengan rerun di sini, bisa menyebabkan loop jika tidak dikelola dengan baik.
                 # Lebih baik set di awal atau pastikan hanya sekali jalan.