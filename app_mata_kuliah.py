import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_mata_kuliah():
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
            cursor.execute("SELECT * FROM mata_kuliah")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    def tambah_data():
        kode_mk = entry_kode.get()
        nama_mk = entry_nama.get()
        sks = entry_sks.get()
        semester = entry_semester.get()

        if not kode_mk or not nama_mk:
            messagebox.showwarning("Warning", "Kode MK dan Nama Mata Kuliah wajib diisi!")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, semester) VALUES (%s, %s, %s, %s)"
            val = (kode_mk, nama_mk, sks, semester)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data mata kuliah berhasil ditambahkan!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
            return

        kode_mk = entry_kode.get()
        nama_mk = entry_nama.get()
        sks = entry_sks.get()
        semester = entry_semester.get()

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "UPDATE mata_kuliah SET nama_mk=%s, sks=%s, semester=%s WHERE kode_mk=%s"
            val = (nama_mk, sks, semester, kode_mk)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data mata kuliah berhasil diperbarui!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
            return

        kode_mk = entry_kode.get()
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus Mata Kuliah {kode_mk}?")
        if confirm:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM mata_kuliah WHERE kode_mk = %s", (kode_mk,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data mata kuliah berhasil dihapus!")
                clear_fields()
                load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def select_item(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            clear_fields()
            entry_kode.insert(0, values[0])
            entry_nama.insert(0, values[1])
            entry_sks.insert(0, values[2])
            entry_semester.insert(0, values[3])

    def clear_fields():
        entry_kode.delete(0, tk.END)
        entry_nama.delete(0, tk.END)
        entry_sks.delete(0, tk.END)
        entry_semester.delete(0, tk.END)

    # --- GUI WINDOW (Menggunakan Toplevel) ---
    window_mk = tk.Toplevel()
    window_mk.title("Aplikasi Data Mata Kuliah - SIAKAD")
    window_mk.geometry("750x500")

    frame_form = tk.LabelFrame(window_mk, text=" Form Data Mata Kuliah ", padx=10, pady=10)
    frame_form.pack(fill="x", padx=15, pady=10)

    labels = ["Kode MK", "Nama Mata Kuliah", "SKS", "Semester"]
    for i, label_text in enumerate(labels):
        tk.Label(frame_form, text=label_text).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=5)

    entry_kode = tk.Entry(frame_form)
    entry_kode.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    entry_nama = tk.Entry(frame_form)
    entry_nama.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    entry_sks = tk.Entry(frame_form)
    entry_sks.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    entry_semester = tk.Entry(frame_form)
    entry_semester.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    frame_form.grid_columnconfigure(1, weight=1)
    frame_form.grid_columnconfigure(3, weight=1)

    # Tombol Aksi
    frame_btn = tk.Frame(window_mk)
    frame_btn.pack(fill="x", padx=15, pady=5)

    tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

    # Tabel Data (Treeview)
    frame_table = tk.Frame(window_mk)
    frame_table.pack(fill="both", expand=True, padx=15, pady=10)

    columns = ("kode_mk", "nama_mk", "sks", "semester")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    headers = ["Kode MK", "Nama Mata Kuliah", "SKS", "Semester"]
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)

    tree.column("kode_mk", width=100)
    tree.column("nama_mk", width=250)
    tree.column("sks", width=80)
    tree.column("semester", width=100)

    tree.bind("<<TreeviewSelect>>", select_item)

    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    load_data()