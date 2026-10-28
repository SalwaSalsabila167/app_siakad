import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def run_krs():
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
            cursor.execute("SELECT * FROM krs")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)
            db.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Gagal mengambil data: {e}")

    def tambah_data():
        id_krs = entry_id.get()
        nim = entry_nim.get()
        kode_mk = entry_mk.get()
        semester = entry_semester.get()
        tahun_ajaran = entry_tahun.get()

        if not id_krs or not nim or not kode_mk:
            messagebox.showwarning("Warning", "ID KRS, NIM, dan Kode MK wajib diisi!")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "INSERT INTO krs (id_krs, nim, kode_mk, semester, tahun_ajaran) VALUES (%s, %s, %s, %s, %s)"
            val = (id_krs, nim, kode_mk, semester, tahun_ajaran)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data KRS berhasil ditambahkan!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {e}")

    def edit_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin diubah!")
            return

        id_krs = entry_id.get()
        nim = entry_nim.get()
        kode_mk = entry_mk.get()
        semester = entry_semester.get()
        tahun_ajaran = entry_tahun.get()

        try:
            db = connect_db()
            cursor = db.cursor()
            sql = "UPDATE krs SET nim=%s, kode_mk=%s, semester=%s, tahun_ajaran=%s WHERE id_krs=%s"
            val = (nim, kode_mk, semester, tahun_ajaran, id_krs)
            cursor.execute(sql, val)
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data KRS berhasil diperbarui!")
            clear_fields()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui data: {e}")

    def hapus_data():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih data di tabel yang ingin dihapus!")
            return

        id_krs = entry_id.get()
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus KRS ID {id_krs}?")
        if confirm:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM krs WHERE id_krs = %s", (id_krs,))
                db.commit()
                db.close()
                messagebox.showinfo("Sukses", "Data KRS berhasil dihapus!")
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
            entry_mk.insert(0, values[2])
            entry_semester.insert(0, values[3])
            entry_tahun.insert(0, values[4])

    def clear_fields():
        entry_id.delete(0, tk.END)
        entry_nim.delete(0, tk.END)
        entry_mk.delete(0, tk.END)
        entry_semester.delete(0, tk.END)
        entry_tahun.delete(0, tk.END)

    # --- GUI WINDOW (Menggunakan Toplevel) ---
    window_krs = tk.Toplevel()
    window_krs.title("Aplikasi Data KRS - SIAKAD")
    window_krs.geometry("750x500")

    frame_form = tk.LabelFrame(window_krs, text=" Form Data KRS ", padx=10, pady=10)
    frame_form.pack(fill="x", padx=15, pady=10)

    labels = ["ID KRS", "NIM Mahasiswa", "Kode MK", "Semester", "Tahun Ajaran"]
    for i, label_text in enumerate(labels):
        tk.Label(frame_form, text=label_text).grid(row=i//2, column=(i%2)*2, sticky="w", padx=5, pady=5)

    entry_id = tk.Entry(frame_form)
    entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    entry_nim = tk.Entry(frame_form)
    entry_nim.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    entry_mk = tk.Entry(frame_form)
    entry_mk.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    entry_semester = tk.Entry(frame_form)
    entry_semester.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

    entry_tahun = tk.Entry(frame_form)
    entry_tahun.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    frame_form.grid_columnconfigure(1, weight=1)
    frame_form.grid_columnconfigure(3, weight=1)

    # Tombol Aksi
    frame_btn = tk.Frame(window_krs)
    frame_btn.pack(fill="x", padx=15, pady=5)

    tk.Button(frame_btn, text="Tambah", bg="#4CAF50", fg="white", command=tambah_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Edit", bg="#2196F3", fg="white", command=edit_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Hapus", bg="#f44336", fg="white", command=hapus_data, width=12).pack(side="left", padx=5)
    tk.Button(frame_btn, text="Clear", bg="#9E9E9E", fg="white", command=clear_fields, width=12).pack(side="left", padx=5)

    # Tabel Data (Treeview)
    frame_table = tk.Frame(window_krs)
    frame_table.pack(fill="both", expand=True, padx=15, pady=10)

    columns = ("id_krs", "nim", "kode_mk", "semester", "tahun_ajaran")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")

    headers = ["ID KRS", "NIM", "Kode MK", "Semester", "Tahun Ajaran"]
    for col, head in zip(columns, headers):
        tree.heading(col, text=head)

    tree.column("id_krs", width=80)
    tree.column("nim", width=110)
    tree.column("kode_mk", width=100)
    tree.column("semester", width=90)
    tree.column("tahun_ajaran", width=110)

    tree.bind("<<TreeviewSelect>>", select_item)

    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    load_data()