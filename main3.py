import streamlit as st


# --- Existing Functions ---
def calculate_new_avg(avg_price, current_price, current_lots, buy_lots):
    """Calculates the new average price after buying additional lots."""
    total_shares_value = (current_lots * avg_price * 100) + (buy_lots * current_price * 100)
    total_lots = current_lots + buy_lots
    if total_lots == 0:
        return 0
    new_avg = total_shares_value / (total_lots * 100)
    return new_avg

def calculate_lots_for_budget(budget, stock_price):
    """Calculates how many lots can be bought with a given budget."""
    if stock_price == 0:
        return 0
    return budget // (stock_price * 100) # Integer division for whole lots

def calculate_profit(target_price, avg_price, total_lots):
    """Calculates potential profit based on target sell price."""
    return (target_price - avg_price) * total_lots * 100

def calculate_percentage_change(current_avg_price, current_market_price):
    """Calculates the percentage upside or downside."""
    if current_avg_price == 0:
        return 0
    percentage = ((current_market_price - current_avg_price) / current_avg_price) * 100
    return percentage

# --- New Functions ---
def calculate_bep(avg_price, total_lots, buy_fee_percentage, sell_fee_percentage):
    """
    Calculates the Break-Even Price (BEP) including buy and sell transaction fees.
    Assumes avg_price is your *current* average price per share.
    """
    if total_lots == 0:
        return 0

    buy_fee_decimal = buy_fee_percentage / 100
    sell_fee_decimal = sell_fee_percentage / 100

    effective_avg_cost_per_share = avg_price * (1 + buy_fee_decimal)

    if (1 - sell_fee_decimal) <= 0: # Avoid division by zero or negative/zero denominator
        return float('inf') # Indicates impossible to break even with such high fees

    bep = effective_avg_cost_per_share / (1 - sell_fee_decimal)
    return bep

def main():
    st.set_page_config(layout="centered")
    st.title("Kalkulator Averaging Saham")
    st.markdown("---")

    # --- Reorganized Menu ---
    st.sidebar.header("Pilih Alat Kalkulasi")
    tool_category = st.sidebar.radio(
        "Kategori:",
        ("Analisis Posisi Saat Ini", "Simulasi & Perencanaan Pembelian")
    )

    st.markdown("---")

    if tool_category == "Analisis Posisi Saat Ini":
        st.subheader("📊 Analisis Posisi Saham Anda Saat Ini")
        analysis_type = st.radio(
            "Pilih jenis analisis:",
            ("Hitung Harga Rata-rata Baru", "Hitung Harga Break-Even (BEP)")
        )

        if analysis_type == "Hitung Harga Rata-rata Baru":
            st.markdown("### 📈 Hitung Harga Rata-rata Baru Saham")
            st.info("Gunakan ini untuk mengetahui harga rata-rata Anda setelah pembelian tambahan.")

            avg_price = st.number_input("Harga Rata-rata Anda Saat Ini (per lembar)", min_value=1, step=1, help="Harga rata-rata pembelian saham Anda saat ini.", key="avg_price_new_avg")
            current_lots = st.number_input("Jumlah Lot Anda Saat Ini", min_value=1, step=1, help="Total lot saham yang sudah Anda miliki.", key="current_lots_new_avg")
            current_price = st.number_input("Harga Saham Saat Ini / Harga Pembelian (per lembar)", min_value=1, step=1, help="Harga saham yang berlaku di pasar saat ini atau harga Anda berencana membeli.", key="current_price_new_avg")

            st.markdown("---")
            st.subheader("Bagaimana Anda ingin menentukan jumlah lot yang dibeli?")
            buy_input_method = st.radio(
                "Pilih metode:",
                ("Masukkan Jumlah Lot", "Masukkan Anggaran (Budget)"),
                key="buy_method"
            )

            buy_lots = 0 # Initialize buy_lots

            if buy_input_method == "Masukkan Jumlah Lot":
                buy_lots = st.number_input("Jumlah Lot yang Ingin Anda Beli", min_value=0, step=1, help="Jumlah lot tambahan yang akan Anda beli.", key="buy_lots_input")
            else: # Masukkan Anggaran (Budget)
                budget_to_buy = st.number_input("Anggaran untuk Pembelian (IDR)", min_value=0, step=1000, help="Total dana yang ingin Anda gunakan untuk pembelian tambahan.", key="budget_input")
                if budget_to_buy > 0 and current_price > 0:
                    calculated_lots = calculate_lots_for_budget(budget_to_buy, current_price)
                    st.info(f"Dengan anggaran **IDR {budget_to_buy:,.0f}** pada harga **Rp {current_price}**, Anda bisa membeli **{calculated_lots} lot**.")
                    buy_lots = calculated_lots
                elif budget_to_buy > 0 and current_price == 0:
                    st.warning("Harga saham tidak boleh nol untuk menghitung lot dari anggaran.")


            if st.button("Hitung Rata-rata Baru", type="primary"):
                if buy_lots == 0:
                    st.info("Anda belum memasukkan jumlah lot yang akan dibeli atau anggaran Anda tidak cukup untuk membeli 1 lot. Harga rata-rata tidak akan berubah.")
                else:
                    new_avg = calculate_new_avg(avg_price, current_price, current_lots, buy_lots)
                    st.success(f"Harga rata-rata baru Anda adalah: **Rp {new_avg:,.2f}** per lembar")
                    st.info(f"Total lot Anda setelah pembelian: **{current_lots + buy_lots} lot**")

        elif analysis_type == "Hitung Harga Break-Even (BEP)":
            st.markdown("### 🎯 Hitung Harga Break-Even (BEP) Saham")
            st.info("BEP adalah harga jual minimal agar Anda tidak rugi, termasuk biaya transaksi.")

            avg_price_bep = st.number_input("Harga Rata-rata Anda Saat Ini (per lembar)", min_value=1, step=1, help="Harga rata-rata pembelian saham Anda.", key="avg_price_bep")
            total_lots_bep = st.number_input("Jumlah Lot Anda Saat Ini", min_value=1, step=1, help="Total lot saham yang Anda miliki.", key="total_lots_bep")

            st.markdown("---")
            st.subheader("Pengaturan Biaya Transaksi (umumnya):")
            buy_fee_percentage = st.number_input("Biaya Beli (%)", value=0.15, min_value=0.0, max_value=5.0, step=0.01, format="%.2f", help="Total biaya saat membeli saham (misal: 0.15% sudah termasuk PPN).", key="buy_fee")
            sell_fee_percentage = st.number_input("Biaya Jual (%)", value=0.25, min_value=0.0, max_value=5.0, step=0.01, format="%.2f", help="Total biaya saat menjual saham (misal: 0.25% sudah termasuk PPN & PPh).", key="sell_fee")
            st.caption("Pastikan untuk memverifikasi biaya ini dengan broker Anda.")


            if st.button("Hitung BEP", type="primary"):
                if avg_price_bep <= 0 or total_lots_bep <= 0:
                    st.warning("Harga rata-rata dan jumlah lot harus lebih dari nol.")
                elif (1 - (sell_fee_percentage / 100)) <= 0:
                    st.error("Biaya jual terlalu tinggi, tidak mungkin mencapai Break-Even Point (BEP).")
                else:
                    bep_price = calculate_bep(avg_price_bep, total_lots_bep, buy_fee_percentage, sell_fee_percentage)
                    st.success(f"Harga Break-Even (BEP) Anda adalah: **Rp {bep_price:,.2f}** per lembar")
                    if bep_price > avg_price_bep:
                        st.info(f"Anda perlu menjual di atas harga rata-rata Anda karena adanya biaya transaksi. Selisih: Rp {(bep_price - avg_price_bep):,.2f}")
                    else:
                        st.info("BEP Anda kurang dari atau sama dengan harga rata-rata Anda (ini mengindikasikan perhitungan mungkin tidak mempertimbangkan semua biaya atau biaya sangat rendah).")

    elif tool_category == "Simulasi & Perencanaan Pembelian":
        st.subheader("🧪 Simulasi & Perencanaan Pembelian Saham")
        planning_type = st.radio(
            "Pilih jenis simulasi/perencanaan:",
            ("Simulasi Skenario Averaging", "Hitung Lot untuk Anggaran")
        )

        if planning_type == "Simulasi Skenario Averaging":
            st.markdown("### 📈 Simulasi Skenario Averaging Saham")
            st.info("Lihat bagaimana pembelian tambahan mempengaruhi harga rata-rata, potensi keuntungan, dan posisi Anda.")

            current_avg_price_sim = st.number_input("Harga Rata-rata Anda Saat Ini (per lembar)", min_value=1, step=1, help="Harga rata-rata pembelian saham Anda saat ini.", key="avg_price_sim")
            current_lots_sim = st.number_input("Jumlah Lot Anda Saat Ini", min_value=1, step=1, help="Total lot saham yang sudah Anda miliki.", key="lots_sim")

            st.markdown("---")
            st.subheader("Skenario Pembelian Tambahan:")
            simulated_buy_price = st.number_input(
                "Harga Saham Saat Ini / Harga Simulasi Pembelian (per lembar)",
                min_value=1,
                step=1,
                help="Harga saham saat ini atau harga di mana Anda ingin mensimulasikan pembelian.",
                key="sim_buy_price"
            )

            additional_lots_sim = st.number_input(
                "Jumlah Lot Tambahan yang Akan Dibeli",
                min_value=0,
                step=1,
                value=1, # Default to 1 lot for easier initial interaction
                help="Berapa banyak lot tambahan yang ingin Anda beli pada harga simulasi.",
                key="add_lots_sim"
            )

            # Automatically run simulation as inputs are changed, no button needed for dynamic updates
            if current_avg_price_sim > 0 and current_lots_sim > 0 and simulated_buy_price > 0:
                new_avg_simulated = calculate_new_avg(current_avg_price_sim, simulated_buy_price, current_lots_sim, additional_lots_sim)
                total_new_lots = current_lots_sim + additional_lots_sim

                # Calculate profit/loss and percentage change against the *new* average price
                # if sold at the *simulated buy price* (or market price)
                profit_loss_at_sim_price = calculate_profit(simulated_buy_price, new_avg_simulated, total_new_lots)
                percentage_change_at_sim_price = calculate_percentage_change(new_avg_simulated, simulated_buy_price)

                st.subheader("Hasil Simulasi:")
                st.write(f"Jika Anda membeli **{additional_lots_sim} lot** pada harga **Rp {simulated_buy_price:,.0f}**:")
                st.metric(label="Harga Rata-rata Baru Anda", value=f"Rp {new_avg_simulated:,.2f}")
                st.metric(label="Total Lot Setelah Pembelian", value=f"{total_new_lots} lot")

                st.markdown("---")
                st.subheader("Dampak pada Posisi Anda (jika dijual pada harga simulasi):")

                if profit_loss_at_sim_price > 0:
                    st.metric(label="Potensi Keuntungan/Kerugian", value=f"IDR {profit_loss_at_sim_price:,.0f}", delta="Keuntungan")
                elif profit_loss_at_sim_price < 0:
                    st.metric(label="Potensi Keuntungan/Kerugian", value=f"IDR {profit_loss_at_sim_price:,.0f}", delta="Rugi", delta_color="inverse")
                else:
                    st.metric(label="Potensi Keuntungan/Kerugian", value=f"IDR {profit_loss_at_sim_price:,.0f}", delta="Impas")

                if percentage_change_at_sim_price > 0:
                    st.metric(label="Persentase Perubahan Harga", value=f"+{percentage_change_at_sim_price:,.2f}%", delta="Untung")
                elif percentage_change_at_sim_price < 0:
                    st.metric(label="Persentase Perubahan Harga", value=f"{percentage_change_at_sim_price:,.2f}%", delta="Rugi", delta_color="inverse")
                else:
                    st.metric(label="Persentase Perubahan Harga", value=f"{percentage_change_at_sim_price:,.2f}%", delta="Impas")
            else:
                st.warning("Mohon masukkan harga rata-rata dan jumlah lot Anda saat ini, serta harga simulasi pembelian.")

        elif planning_type == "Hitung Lot untuk Anggaran":
            st.markdown("### 💰 Hitung Jumlah Lot yang Bisa Dibeli")
            st.info("Tentukan berapa banyak lot saham yang bisa Anda beli dengan anggaran tertentu.")
            budget = st.number_input("Anggaran Anda (IDR)", min_value=0, step=1000, help="Total dana yang ingin Anda gunakan untuk membeli saham.", key="budget_lots")
            current_price = st.number_input("Harga Saham Saat Ini (per lembar)", min_value=1, step=1, help="Harga saham yang berlaku di pasar saat ini.", key="price_lots")

            if st.button("Hitung Lot", type="primary"):
                if budget == 0:
                    st.warning("Mohon masukkan anggaran Anda.")
                elif current_price == 0:
                    st.warning("Harga saham tidak boleh nol.")
                else:
                    possible_lots = calculate_lots_for_budget(budget, current_price)
                    cost_per_lot = current_price * 100
                    if possible_lots > 0:
                        st.success(f"Dengan anggaran **IDR {budget:,.0f}** dan harga saham **Rp {current_price}**, Anda bisa membeli **{possible_lots} lot**.")
                        st.info(f"Setiap lot adalah 100 lembar saham. Biaya per lot adalah **Rp {cost_per_lot:,.0f}**.")
                        st.info(f"Total biaya pembelian **{possible_lots} lot** adalah **IDR {(possible_lots * cost_per_lot):,.0f}**.")
                    else:
                        st.warning("Anggaran Anda tidak cukup untuk membeli 1 lot saham.")


if __name__ == "__main__":
    main()