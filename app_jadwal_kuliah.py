import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_jadwal_kuliah():
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
            cursor.execute("SELECT * FROM jadwal_kuliah")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    def tambah_data():
        id_jadwal = entry_id.get()
        kode_mk = entry_mk.get()
        nip = entry_nip.get()
        hari = combo_hari.get()
        jam = entry_jam.get()
        ruangan = entry_ruangan.get()

        if not id_jadwal or not kode_mk or not nip:
            messagebox.showwarning("Warning", "ID Jadwal, Kode MK, dan NIP Dosen wajib diisi!")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO jadwal_kuliah (id_jadwal, kode_mk, nip, hari, jam, ruangan) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (id_jadwal, kode_mk, nip, hari, jam, ruangan)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data jadwal kuliah berhasil ditambahkan!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
            return

        id_jadwal = entry_id.get()
        kode_mk = entry_mk.get()
        nip = entry_nip.get()
        hari = combo_hari.get()
        jam = entry_jam.get()
        ruangan = entry_ruangan.get()

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "UPDATE jadwal_kuliah SET kode_mk=%s, nip=%s, hari=%s, jam=%s, ruangan=%s WHERE id_jadwal=%s"
            val = (kode_mk, nip, hari, jam, ruangan, id_jadwal)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data jadwal kuliah berhasil diperbarui!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
            return

        id_jadwal = entry_id.get()
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus Jadwal ID {id_jadwal}?")
        if confirm:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM jadwal_kuliah WHERE id_jadwal = %s", (id_jadwal,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data jadwal kuliah berhasil dihapus!")
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
            entry_mk.insert(0, values[1])
            entry_nip.insert(0, values[2])
            combo_hari.set(values[3])
            entry_jam.insert(0, values[4])
            entry_ruangan.insert(0, values[5])

    def clear_fields():
        entry_id.delete(0, tk.END)
        entry_mk.delete(0, tk.END)
        entry_nip.delete(0, tk.END)
        combo_hari.set("")
        entry_jam.delete(0, tk.END)
        entry_ruangan.delete(0, tk.END)

    # --- GUI WINDOW (Menggunakan Toplevel) ---
    window_jadwal = tk.Toplevel()
    window_jadwal.title("Aplikasi Jadwal Kuliah - SIAKAD")
    window_jadwal.geometry("800x550")

    frame_form = tk.LabelFrame(window_jadwal, text=" Form Data Jadwal Kuliah ", padx=10, pady=10)
    frame_form.pack(fill="x", padx=15, pady=10)

    labels = ["ID Jadwal", "Kode MK", "NIP Dosen", "Hari", "Jam", "Ruangan"]
    for i, label_text in enumerate(labels):
        tk.Label(frame_form, text=label_text).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=5)

    entry_id = tk.Entry(frame_form)
    entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    entry_mk = tk.Entry(frame_form)
    entry_mk.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    entry_nip = tk.Entry(frame_form)
    entry_nip.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    combo_hari = ttk.Combobox(frame_form, values=["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"], state="readonly")
    combo_hari.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    entry_jam = tk.Entry(frame_form)
    entry_jam.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    entry_ruangan = tk.Entry(frame_form)
    entry_ruangan.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

    frame_form.grid_columnconfigure(1, weight=1)
    frame_form.grid_columnconfigure(3, weight=1)

    # Tombol Aksi
    frame_btn = tk.Frame(window_jadwal)
    frame_btn.pack(fill="x", padx=15, pady=5)

    tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

    # Tabel Data (Treeview)
    frame_table = tk.Frame(window_jadwal)
    frame_table.pack(fill="both", expand=True, padx=15, pady=10)

    columns = ("id_jadwal", "kode_mk", "nip", "hari", "jam", "ruangan")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    headers = ["ID Jadwal", "Kode MK", "NIP Dosen", "Hari", "Jam", "Ruangan"]
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)

    tree.column("id_jadwal", width=80)
    tree.column("kode_mk", width=90)
    tree.column("nip", width=120)
    tree.column("hari", width=90)
    tree.column("jam", width=100)
    tree.column("ruangan", width=90)

    tree.bind("<<TreeviewSelect>>", select_item)

    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    load_data()