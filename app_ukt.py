import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_pembayaran():
    # --- KONEKSI DATABASE ---
    def connect_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="siakad"
        )

    # --- FUNGSI CRUD ---
    def load_data():
        for row in tree.get_children():
            tree.delete(row)
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM pembayaran_ukt")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    def tambah_data():
        id_bayar = entry_id.get()
        nim = entry_nim.get()
        jumlah = entry_jumlah.get()
        tanggal = entry_tanggal.get()
        status = combo_status.get()

        if not id_bayar or not nim or not jumlah:
            messagebox.showwarning("Warning", "ID Bayar, NIM, dan Jumlah UKT wajib diisi!")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO pembayaran_ukt (id_pembayaran, nim, jumlah, tanggal_bayar, status) VALUES (%s, %s, %s, %s, %s)"
            val = (id_bayar, nim, jumlah, tanggal, status)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data pembayaran UKT berhasil ditambahkan!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
            return

        id_bayar = entry_id.get()
        nim = entry_nim.get()
        jumlah = entry_jumlah.get()
        tanggal = entry_tanggal.get()
        status = combo_status.get()

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "UPDATE pembayaran_ukt SET nim=%s, jumlah=%s, tanggal_bayar=%s, status=%s WHERE id_pembayaran=%s"
            val = (nim, jumlah, tanggal, status, id_bayar)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data pembayaran UKT berhasil diperbarui!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
            return

        id_bayar = entry_id.get()
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus Pembayaran ID {id_bayar}?")
        if confirm:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM pembayaran_ukt WHERE id_pembayaran = %s", (id_bayar,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data pembayaran UKT berhasil dihapus!")
                clear_fields()
                load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            clear_fields()
            entry_id.insert(0, values[0])
            entry_nim.insert(0, values[1])
            entry_jumlah.insert(0, values[2])
            entry_tanggal.insert(0, values[3])
            combo_status.set(values[4])

    def clear_fields():
        entry_id.delete(0, tk.END)
        entry_nim.delete(0, tk.END)
        entry_jumlah.delete(0, tk.END)
        entry_tanggal.delete(0, tk.END)
        combo_status.set("")

    # --- GUI WINDOW (Menggunakan Toplevel) ---
    window_bayar = tk.Toplevel()
    window_bayar.title("Aplikasi Pembayaran UKT - SIAKAD")
    window_bayar.geometry("750x500")

    frame_form = tk.LabelFrame(window_bayar, text=" Form Pembayaran UKT ", padx=10, pady=10)
    frame_form.pack(fill="x", padx=15, pady=10)

    labels = ["ID Pembayaran", "NIM Mahasiswa", "Jumlah (Rp)", "Tanggal Bayar (YYYY-MM-DD)", "Status"]
    for i, label_text in enumerate(labels):
        tk.Label(frame_form, text=label_text).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=5)

    entry_id = tk.Entry(frame_form)
    entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    entry_nim = tk.Entry(frame_form)
    entry_nim.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    entry_jumlah = tk.Entry(frame_form)
    entry_jumlah.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    entry_tanggal = tk.Entry(frame_form)
    entry_tanggal.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    combo_status = ttk.Combobox(frame_form, values=["Lunas", "Belum Lunas", "Pending"], state="readonly")
    combo_status.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    frame_form.grid_columnconfigure(1, weight=1)
    frame_form.grid_columnconfigure(3, weight=1)

    # Tombol Aksi
    frame_btn = tk.Frame(window_bayar)
    frame_btn.pack(fill="x", padx=15, pady=5)

    tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

    # Tabel Data (Treeview)
    frame_table = tk.Frame(window_bayar)
    frame_table.pack(fill="both", expand=True, padx=15, pady=10)

    columns = ("id_pembayaran", "nim", "jumlah", "tanggal_bayar", "status")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    headers = ["ID Pembayaran", "NIM", "Jumlah", "Tanggal Bayar", "Status"]
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)

    tree.column("id_pembayaran", width=90)
    tree.column("nim", width=110)
    tree.column("jumlah", width=110)
    tree.column("tanggal_bayar", width=110)
    tree.column("status", width=100)

    tree.bind("<<TreeviewSelect>>", select_item)

    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    load_data()