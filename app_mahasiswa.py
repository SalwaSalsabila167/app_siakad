import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_mahasiswa():
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
            cursor.execute("SELECT * FROM mahasiswa")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    def tambah_data():
        nim = entry_nim.get()
        nama = entry_nama.get()
        jk = combo_jk.get()
        tgl_lahir = entry_tgl.get()
        tmpt_lahir = entry_tmpt.get()
        alamat = entry_alamat.get()
        tlp = entry_tlp.get()
        email = entry_email.get()
        jurusan = entry_jurusan.get()
        angkatan = entry_angkatan.get()
        status = combo_status.get()

        if not nim or not nama:
            messagebox.showwarning("Warning", "NIM dan Nama Lengkap wajib diisi!")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = """INSERT INTO mahasiswa (nim, nama_lengkap, jenis_kelamin, tanggal_lahir, tempat_lahir, alamat, no_telepon, email, jurusan, angkatan, status) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (nim, nama, jk, tgl_lahir, tmpt_lahir, alamat, tlp, email, jurusan, angkatan, status)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
            return

        nim = entry_nim.get()
        nama = entry_nama.get()
        jk = combo_jk.get()
        tgl_lahir = entry_tgl.get()
        tmpt_lahir = entry_tmpt.get()
        alamat = entry_alamat.get()
        tlp = entry_tlp.get()
        email = entry_email.get()
        jurusan = entry_jurusan.get()
        angkatan = entry_angkatan.get()
        status = combo_status.get()

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = """UPDATE mahasiswa SET nama_lengkap=%s, jenis_kelamin=%s, tanggal_lahir=%s, tempat_lahir=%s, 
                     alamat=%s, no_telepon=%s, email=%s, jurusan=%s, angkatan=%s, status=%s WHERE nim=%s"""
            val = (nama, jk, tgl_lahir, tmpt_lahir, alamat, tlp, email, jurusan, angkatan, status, nim)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil diperbarui!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
            return

        nim = entry_nim.get()
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus mahasiswa NIM {nim}?")
        if confirm:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data mahasiswa berhasil dihapus!")
                clear_fields()
                load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            clear_fields()
            entry_nim.insert(0, values[0])
            entry_nama.insert(0, values[1])
            combo_jk.set(values[2])
            entry_tgl.insert(0, values[3])
            entry_tmpt.insert(0, values[4])
            entry_alamat.insert(0, values[5])
            entry_tlp.insert(0, values[6])
            entry_email.insert(0, values[7])
            entry_jurusan.insert(0, values[8])
            entry_angkatan.insert(0, values[9])
            combo_status.set(values[10])

    def clear_fields():
        entry_nim.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        combo_jk.set("")
        entry_tgl.delete(0, tk.END)
        entry_tmpt.delete(0, tk.END)
        entry_alamat.delete(0, tk.END)
        entry_tlp.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_jurusan.delete(0, tk.END)
        entry_angkatan.delete(0, tk.END)
        combo_status.set("")

    # --- GUI WINDOW (Menggunakan Toplevel) ---
    window_mhs = tk.Toplevel()
    window_mhs.title("Aplikasi Data Mahasiswa - SIAKAD")
    window_mhs.geometry("1000x650")

    frame_form = tk.LabelFrame(window_mhs, text=" Form Data Mahasiswa ", padx=10, pady=10)
    frame_form.pack(fill="x", padx=15, pady=10)

    labels = [
        "NIM", "Nama Lengkap", "Jenis Kelamin", "Tanggal Lahir (YYYY-MM-DD)", 
        "Tempat Lahir", "Alamat", "No Telepon", "Email", 
        "Jurusan", "Angkatan", "Status"
    ]

    for i, label_text in enumerate(labels):
        tk.Label(frame_form, text=label_text).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=3)

    entry_nim = tk.Entry(frame_form)
    entry_nim.grid(row=0, column=1, padx=5, pady=3, sticky="ew")

    entry_nama = tk.Entry(frame_form)
    entry_nama.grid(row=0, column=3, padx=5, pady=3, sticky="ew")

    combo_jk = ttk.Combobox(frame_form, values=["Laki-laki", "Perempuan"], state="readonly")
    combo_jk.grid(row=1, column=1, padx=5, pady=3, sticky="ew")

    entry_tgl = tk.Entry(frame_form)
    entry_tgl.grid(row=1, column=3, padx=5, pady=3, sticky="ew")

    entry_tmpt = tk.Entry(frame_form)
    entry_tmpt.grid(row=2, column=1, padx=5, pady=3, sticky="ew")

    entry_alamat = tk.Entry(frame_form)
    entry_alamat.grid(row=2, column=3, padx=5, pady=3, sticky="ew")

    entry_tlp = tk.Entry(frame_form)
    entry_tlp.grid(row=3, column=1, padx=5, pady=3, sticky="ew")

    entry_email = tk.Entry(frame_form)
    entry_email.grid(row=3, column=3, padx=5, pady=3, sticky="ew")

    entry_jurusan = tk.Entry(frame_form)
    entry_jurusan.grid(row=4, column=1, padx=5, pady=3, sticky="ew")

    entry_angkatan = tk.Entry(frame_form)
    entry_angkatan.grid(row=4, column=3, padx=5, pady=3, sticky="ew")

    combo_status = ttk.Combobox(frame_form, values=["Aktif", "Cuti", "Lulus", "Keluar"], state="readonly")
    combo_status.grid(row=5, column=1, padx=5, pady=3, sticky="ew")

    frame_form.grid_columnconfigure(1, weight=1)
    frame_form.grid_columnconfigure(3, weight=1)

    # Tombol Aksi
    frame_btn = tk.Frame(window_mhs)
    frame_btn.pack(fill="x", padx=15, pady=5)

    tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

    # Tabel Data (Treeview)
    frame_table = tk.Frame(window_mhs)
    frame_table.pack(fill="both", expand=True, padx=15, pady=10)

    columns = ("nim", "nama_lengkap", "jenis_kelamin", "tanggal_lahir", "tempat_lahir", "alamat", "no_telepon", "email", "jurusan", "angkatan", "status")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    headers = ["NIM", "Nama Lengkap", "JK", "Tgl Lahir", "Tempat Lahir", "Alamat", "No Telepon", "Email", "Jurusan", "Angkatan", "Status"]
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)

    tree.column("nim", width=80)
    tree.column("nama_lengkap", width=130)
    tree.column("jenis_kelamin", width=80)
    tree.column("tanggal_lahir", width=90)
    tree.column("tempat_lahir", width=90)
    tree.column("alamat", width=150)
    tree.column("no_telepon", width=100)
    tree.column("email", width=130)
    tree.column("jurusan", width=110)
    tree.column("angkatan", width=70)
    tree.column("status", width=70)

    tree.bind("<<TreeviewSelect>>", select_item)

    scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    load_data()