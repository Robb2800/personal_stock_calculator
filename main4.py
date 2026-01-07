import streamlit as st

# --- Fungsi Logika ---
def calculate_metrics(current_avg, current_lots, buy_price, buy_lots, buy_fee_pct, sell_fee_pct, target_sell_price):
    """Menghitung metrik investasi dengan memperhitungkan biaya transaksi."""
    b_fee = buy_fee_pct / 100
    s_fee = sell_fee_pct / 100

    current_shares = current_lots * 100
    current_cost = current_shares * current_avg

    new_shares = buy_lots * 100
    new_buy_value = new_shares * buy_price
    new_buy_cost_total = new_buy_value * (1 + b_fee)

    total_shares = current_shares + new_shares
    total_cost_basis = current_cost + new_buy_cost_total

    if total_shares == 0: return 0, 0, 0, 0, 0

    new_avg = total_cost_basis / total_shares
    bep = new_avg / (1 - s_fee)

    total_sell_value = total_shares * target_sell_price
    net_sell_proceeds = total_sell_value * (1 - s_fee)
    pnl_nominal = net_sell_proceeds - total_cost_basis
    pnl_percent = (pnl_nominal / total_cost_basis) * 100 if total_cost_basis > 0 else 0

    return new_avg, bep, total_shares // 100, pnl_nominal, pnl_percent

def main():
    st.set_page_config(page_title="Stock Master Pro", layout="wide")

    if 'buy_lots' not in st.session_state:
        st.session_state.buy_lots = 0

    # --- HEADER & INSTRUKSI ---
    st.title("📈 Stock Calculator")

    st.info("""
    **💡 Cara Penggunaan:**
    1. **Portofolio:** Masukkan harga rata-rata dan lot Anda di **Sidebar**.
    2. **Pilih Sekuritas:** Fee beli & jual akan menyesuaikan otomatis berdasarkan broker yang Anda pilih.
    3. **Simulasi Transaksi:** Masukkan rencana beli & jual untuk melihat **Rata-rata Baru** dan **Potensi Profit Bersih**.
    """)

    st.markdown("---")

    # --- SIDEBAR: DATA PORTOFOLIO & SEKURITAS ---
    with st.sidebar:
        st.header("📂 Portfolio")
        curr_avg = st.number_input("Harga Rata-rata (Avg)", min_value=0, step=1, value=1000)
        curr_lots = st.number_input("Jumlah Lot", min_value=0, step=1, value=10)

        st.header("🏢 Pilih Sekuritas")
        # Kamus data sekuritas
        broker_data = {
            "XL (Stockbit)": {"beli": 0.15, "jual": 0.25},
            "XC (Ajaib)": {"beli": 0.10, "jual": 0.20},
            "PD (IPOT)": {"beli": 0.19, "jual": 0.29},
            "CP (Valbury)": {"beli": 0.15, "jual": 0.25},
            "SQ (BCA)": {"beli": 0.18, "jual": 0.28},
            "YP (Mirae Asset)": {"beli": 0.15, "jual": 0.25},
            "YB (Yakin Bertumbuh)": {"beli": 0.15, "jual": 0.25}
        }

        selected_broker = st.selectbox("Sekuritas Anda:", list(broker_data.keys()))

        # Ambil fee berdasarkan pilihan
        fee_buy = broker_data[selected_broker]["beli"]
        fee_sell = broker_data[selected_broker]["jual"]

        # Tampilkan fee (hanya baca)
        st.write(f"Fee Beli: **{fee_buy}%**")
        st.write(f"Fee Jual: **{fee_sell}%**")
        st.caption("Fee di atas sudah otomatis digunakan dalam perhitungan.")

    # --- AREA 1: KALKULATOR BUDGET ---
    with st.expander("💰 Kalkulator Budget", expanded=False):
        bg_col1, bg_col2, bg_col3 = st.columns([2, 2, 1])
        with bg_col1:
            my_budget = st.number_input("Modal Tersedia (IDR)", min_value=0, step=100000)
        with bg_col2:
            est_price = st.number_input("Asumsi Harga Beli", min_value=1, value=1000)

        price_per_lot_with_fee = (est_price * 100) * (1 + (fee_buy/100))
        max_lots_possible = int(my_budget // price_per_lot_with_fee) if price_per_lot_with_fee > 0 else 0

        with bg_col3:
            st.write("")
            if st.button("Terapkan Lot", use_container_width=True):
                st.session_state.buy_lots = max_lots_possible

        if my_budget > 0:
            st.success(f"Maksimal Pembelian: **{max_lots_possible} Lot** (Total Biaya: Rp {max_lots_possible * price_per_lot_with_fee:,.0f})")

    # --- AREA 2: SIMULASI & HASIL ---
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.subheader("🔄 Simulasi Transaksi")
        buy_p = st.number_input("Harga Pembelian Baru", min_value=1, step=1, value=1000)
        buy_l = st.number_input("Jumlah Lot Baru", min_value=0, step=1, key="buy_lots")

        st.markdown("---")
        target_s = st.number_input("Target Harga Jual", min_value=1, step=1, value=buy_p + 100)

    # Hitung metrik akhir
    new_avg, bep, total_lots, pnl_nom, pnl_pct = calculate_metrics(
        curr_avg, curr_lots, buy_p, buy_l, fee_buy, fee_sell, target_s
    )

    with col_right:
        st.subheader("📊 Hasil Analisis")

        res_col1, res_col2 = st.columns(2)
        res_col1.metric("Rata-rata Baru", f"Rp {new_avg:,.2f}")
        res_col2.metric("Titik Impas (BEP)", f"Rp {bep:,.2f}",help="Harga jual agar tidak rugi setelah dipotong fee.")

        st.markdown("---")
        st.write("**Potensi Keuntungan/Kerugian Bersih:**")
        p_color = "normal" if pnl_nom >= 0 else "inverse"
        st.metric(label="Net Profit/Loss", value=f"Rp {pnl_nom:,.0f}", delta=f"{pnl_pct:.2f}%", delta_color=p_color)

        st.info(f"Total Kepemilikan: **{total_lots} Lot** | Estimasi Nilai: **Rp {total_lots * new_avg * 100:,.0f}**")

if __name__ == "__main__":
    main()