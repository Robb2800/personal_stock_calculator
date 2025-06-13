import streamlit as st

def calculate_new_avg(avg_price, current_price, current_lots, buy_lots):
  
    total_shares_value = (current_lots * avg_price * 100) + (buy_lots * current_price * 100)
    total_lots = current_lots + buy_lots
    new_avg = total_shares_value / (total_lots * 100)
    return new_avg

def calculate_lots_for_budget(budget, stock_price):

    return budget // (stock_price * 100)

def calculate_profit(target_price, avg_price, total_lots):
   
    return (target_price - avg_price) * total_lots * 100

def main():
    st.set_page_config(layout="centered") 
    st.title("Kalkulator Averaging Saham")
    st.markdown("---")


    st.subheader("Pilih jenis kalkulasi:")
    calculation_type = st.radio(
        "Pilih salah satu opsi di bawah:",
        ("Hitung Harga Rata-rata Baru", "Hitung Lot untuk Anggaran", "Hitung Potensi Keuntungan")
    )

    st.markdown("---")

    if calculation_type == "Hitung Harga Rata-rata Baru":
        st.subheader("📈 Hitung Harga Rata-rata Baru Saham")
        avg_price = st.number_input("Harga Rata-rata Anda Saat Ini (per lembar)", min_value=1, step=1, help="Harga rata-rata pembelian saham Anda saat ini.")
        current_price = st.number_input("Harga Saham Saat Ini (per lembar)", min_value=1, step=1, help="Harga saham yang berlaku di pasar saat ini.")
        current_lots = st.number_input("Jumlah Lot Anda Saat Ini", min_value=1, step=1, help="Total lot saham yang sudah Anda miliki.")
        buy_lots = st.number_input("Jumlah Lot yang Ingin Anda Beli", min_value=0, step=1, help="Jumlah lot tambahan yang akan Anda beli.")

        if st.button("Hitung Rata-rata Baru", type="primary"):
            if buy_lots == 0:
                st.info("Anda belum memasukkan jumlah lot yang akan dibeli. Harga rata-rata tidak akan berubah.")
            else:
                new_avg = calculate_new_avg(avg_price, current_price, current_lots, buy_lots)
                st.success(f"Harga rata-rata baru Anda adalah: **Rp {new_avg:,.2f}** per lembar")
                st.info(f"Total lot Anda setelah pembelian: **{current_lots + buy_lots} lot**")

    elif calculation_type == "Hitung Lot untuk Anggaran":
        st.subheader("💰 Hitung Jumlah Lot yang Bisa Dibeli")
        budget = st.number_input("Anggaran Anda (IDR)", min_value=0, step=1000, help="Total dana yang ingin Anda gunakan untuk membeli saham.")
        current_price = st.number_input("Harga Saham Saat Ini (per lembar)", min_value=1, step=1, help="Harga saham yang berlaku di pasar saat ini.")

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

    elif calculation_type == "Hitung Potensi Keuntungan":
        st.subheader("💸 Hitung Potensi Keuntungan")
        avg_price = st.number_input("Harga Rata-rata Saham Anda (per lembar)", min_value=1, step=1, help="Harga rata-rata pembelian saham Anda.")
        target_price = st.number_input("Harga Target Jual (per lembar)", min_value=1, step=1, help="Harga yang Anda harapkan untuk menjual saham.")
        total_lots = st.number_input("Total Lot Saham yang Dimiliki", min_value=1, step=1, help="Jumlah total lot saham yang Anda miliki saat ini.")

        if st.button("Hitung Keuntungan", type="primary"):
            if target_price <= avg_price:
                st.warning("Harga target harus lebih tinggi dari harga rata-rata untuk mendapatkan keuntungan.")
            else:
                profit = calculate_profit(target_price, avg_price, total_lots)
                st.success(f"Potensi keuntungan Anda jika harga mencapai **Rp {target_price}** adalah: **IDR {profit:,.0f}**")
                st.info(f"Keuntungan per lembar saham: **IDR {target_price - avg_price:,.0f}**")


if __name__ == "__main__":
    main()