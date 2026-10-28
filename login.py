
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Mengimpor modul file CRUD Dosen dan Mahasiswa yang sudah dibuat sebelumnya
import app_dosen
import app_mahasiswa
import app_mata_kuliah
import app_jadwal_kuliah
import app_krs
import app_ukt

# Deklarasi kelas utama untuk mengelola antarmuka (GUI) jendela login
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SIAKAD Login - Coquette Pink Edition")

        # Membuat jendela login langsung memenuhi layar
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)

        self.root.resizable(True, True)

        #Tema warna pink pastel aestetic
        self.BG_COLOR = "#FFF5F8"
        self.ACCENT_COLOR = "#C76D8A"
        self.BTN_HOVER = "#AD526F"
        self.BOX_BG = "#FFFFFF"

        # Warna tambahan untuk tema Coquette Pink
        self.PINK_LIGHT = "#F9E0E8"
        self.PINK_PALE = "#FFF0F4"
        self.TEXT_COLOR = "#704656"
        self.MUTED_COLOR = "#A17D8B"
        self.BORDER_COLOR = "#F0CFDA"

        self.root.configure(bg=self.BG_COLOR)

        # Konfigurasi koneksi database MySQL
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'siakad'
        }

        # Membuat container/frame utama untuk menampung seluruh elemen visual
        main_frame = tk.Frame(
            self.root,
            bg=self.BG_COLOR
        )
        main_frame.pack(expand=True, fill=tk.BOTH, padx=25, pady=25)

        # Panel login di tengah layar
        login_card = tk.Frame(
            main_frame,
            bg=self.BOX_BG,
            highlightbackground=self.BORDER_COLOR,
            highlightthickness=1,
            padx=45,
            pady=35
        )
        login_card.place(relx=0.5, rely=0.5, anchor="center")

        # Hiasan pita dan ornamen khas Coquette Pink
        tk.Label(
            login_card,
            text="୨୧  ♡  ୨୧",
            font=("Segoe UI", 18),
            bg=self.BOX_BG,
            fg=self.ACCENT_COLOR
        ).pack(pady=(0, 8))

        # Membuat elemen teks/label judul utama form login
        lbl_title = tk.Label(
            login_card,
            text="SIAKAD",
            font=("Georgia", 28, "bold"),
            bg=self.BOX_BG,
            fg=self.ACCENT_COLOR
        )
        lbl_title.pack()

        tk.Label(
            login_card,
            text="SISTEM INFORMASI AKADEMIK",
            font=("Segoe UI", 9, "bold"),
            bg=self.BOX_BG,
            fg=self.MUTED_COLOR
        ).pack(pady=(2, 5))

        tk.Label(
            login_card,
            text="♡  Welcome back!  ♡",
            font=("Georgia", 12, "italic"),
            bg=self.BOX_BG,
            fg=self.TEXT_COLOR
        ).pack(pady=(0, 24))

        # Membuat sub-frame khusus untuk menyusun label dan input teks menggunakan tata letak Grid
        form_frame = tk.Frame(login_card, bg=self.BOX_BG)
        form_frame.pack(fill=tk.X)

        # Baris 0: Label petunjuk input Username (NIP)
        lbl_user = tk.Label(
            form_frame,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=self.BOX_BG,
            fg=self.TEXT_COLOR,
            anchor="w"
        )
        lbl_user.grid(row=0, column=0, padx=2, pady=(0, 5), sticky="w")

        self.entry_nip = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            width=30,
            relief=tk.FLAT,
            bd=0,
            bg=self.PINK_PALE,
            fg=self.TEXT_COLOR,
            insertbackground=self.ACCENT_COLOR
        )
        self.entry_nip.grid(
            row=1, column=0,
            padx=0, pady=(0, 15),
            ipady=10, sticky="ew"
        )
        self.entry_nip.focus()

        # Baris 1: Label petunjuk input Password (Email)
        lbl_pass = tk.Label(
            form_frame,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=self.BOX_BG,
            fg=self.TEXT_COLOR,
            anchor="w"
        )
        lbl_pass.grid(row=2, column=0, padx=2, pady=(0, 5), sticky="w")

        self.entry_email = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            width=30,
            show="*",
            relief=tk.FLAT,
            bd=0,
            bg=self.PINK_PALE,
            fg=self.TEXT_COLOR,
            insertbackground=self.ACCENT_COLOR
        )
        self.entry_email.grid(
            row=3, column=0,
            padx=0, pady=(0, 8),
            ipady=10, sticky="ew"
        )

        form_frame.grid_columnconfigure(0, weight=1)

        # Membuat tombol (button) untuk eksekusi tindakan login
        btn_login = tk.Button(
            login_card,
            text="♡   LOGIN   ♡",
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT_COLOR,
            fg="white",
            activebackground=self.BTN_HOVER,
            activeforeground="white",
            width=25,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.proses_login
        )
        btn_login.pack(fill=tk.X, ipady=9, pady=(20, 12))

        # Efek hover tombol login
        btn_login.bind(
            "<Enter>",
            lambda event: btn_login.config(bg=self.BTN_HOVER)
        )
        btn_login.bind(
            "<Leave>",
            lambda event: btn_login.config(bg=self.ACCENT_COLOR)
        )

        tk.Label(
            login_card,
            text="Made with ♡ and a little pink magic",
            font=("Segoe UI", 9, "italic"),
            bg=self.BOX_BG,
            fg=self.MUTED_COLOR
        ).pack(pady=(5, 0))

        # Mengikat (binding) tombol 'Enter' pada keyboard untuk menjalankan fungsi proses_login()
        self.root.bind('<Return>', lambda event: self.proses_login())

    # Metode untuk menangani alur verifikasi data login pengampu
    def proses_login(self):
        nip = self.entry_nip.get().strip()
        email = self.entry_email.get().strip()

        if not nip or not email:
            messagebox.showwarning(
                "Peringatan",
                "Username (NIP) dan Password (Email) wajib diisi!"
            )
            return

        conn = None
        cursor = None

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)

            query = "SELECT nip, nama_dosen, email FROM dosen WHERE nip = %s AND email = %s"
            cursor.execute(query, (nip, email))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo(
                    "Berhasil",
                    f"Login berhasil!\nSelamat datang, {user['nama_dosen']}."
                )
                # Memanggil fungsi buka_dashboard setelah login sukses
                self.buka_dashboard(user)
            else:
                messagebox.showerror(
                    "Gagal",
                    "Login gagal! Username atau Password salah."
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Koneksi database bermasalah:\n{err}"
            )
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # Metode untuk membuka Menu Utama / Dashboard setelah login berhasil
    def buka_dashboard(self, user):
        # Menutup jendela login
        self.root.destroy()

        # Membuat Jendela Baru untuk Menu Utama SIAKAD
        dashboard = tk.Tk()
        dashboard.title("SIAKAD - Coquette Pink Dashboard")

        # Membuat dashboard langsung memenuhi layar
        try:
            dashboard.state("zoomed")
        except tk.TclError:
            dashboard.attributes("-zoomed", True)

        dashboard.configure(bg=self.BG_COLOR)

        # Membuat layout utama dashboard
        # Sidebar berada di kiri, sedangkan konten utama berada di kanan
        dashboard.grid_rowconfigure(0, weight=1)
        dashboard.grid_columnconfigure(1, weight=1)

        # Sidebar navigasi
        sidebar = tk.Frame(
            dashboard,
            bg=self.ACCENT_COLOR,
            width=255
        )
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        tk.Label(
            sidebar,
            text="୨୧  ♡  ୨୧",
            font=("Segoe UI", 20),
            bg=self.ACCENT_COLOR,
            fg="white"
        ).pack(pady=(35, 5))

        tk.Label(
            sidebar,
            text="SIAKAD",
            font=("Georgia", 25, "bold"),
            bg=self.ACCENT_COLOR,
            fg="white"
        ).pack()

        tk.Label(
            sidebar,
            text="ACADEMIC PORTAL",
            font=("Segoe UI", 9, "bold"),
            bg=self.ACCENT_COLOR,
            fg="#FFEAF0"
        ).pack(pady=(3, 30))

        tk.Frame(
            sidebar,
            bg="#E9AFC2",
            height=1
        ).pack(fill=tk.X, padx=25, pady=(0, 20))

        tk.Label(
            sidebar,
            text="MAIN MENU",
            font=("Segoe UI", 9, "bold"),
            bg=self.ACCENT_COLOR,
            fg="#FFE4EC",
            anchor="w"
        ).pack(fill=tk.X, padx=25, pady=(0, 10))

        # Sapaan pengguna di sidebar
        tk.Label(
            sidebar,
            text=f"♡  {user['nama_dosen']}",
            font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT_COLOR,
            fg="white",
            wraplength=205,
            justify="left",
            anchor="w"
        ).pack(fill=tk.X, padx=22, pady=(0, 20))

        # Sapaan nama dosen yang sedang login
        # Fungsi-fungsi pemanggil modul CRUD
        def buka_form_dosen(): app_dosen.run_dosen()
        def buka_form_mahasiswa(): app_mahasiswa.run_mahasiswa()
        def buka_form_mk(): app_mata_kuliah.run_mata_kuliah()
        def buka_form_jadwal(): app_jadwal_kuliah.run_jadwal_kuliah()
        def buka_form_krs(): app_krs.run_krs()
        def buka_form_ukt(): app_ukt.run_pembayaran()

        # Membuat tombol navigasi pada sidebar
        def buat_tombol_sidebar(teks, perintah):
            tombol = tk.Button(
                sidebar,
                text=teks,
                font=("Segoe UI", 10, "bold"),
                bg=self.ACCENT_COLOR,
                fg="white",
                activebackground=self.BTN_HOVER,
                activeforeground="white",
                relief=tk.FLAT,
                bd=0,
                anchor="w",
                padx=22,
                pady=12,
                cursor="hand2",
                command=perintah
            )
            tombol.pack(fill=tk.X, padx=12, pady=3)

            tombol.bind(
                "<Enter>",
                lambda event: tombol.config(bg=self.BTN_HOVER)
            )
            tombol.bind(
                "<Leave>",
                lambda event: tombol.config(bg=self.ACCENT_COLOR)
            )

        buat_tombol_sidebar("♡  Dashboard", lambda: None)
        buat_tombol_sidebar("♡  Data Dosen", buka_form_dosen)
        buat_tombol_sidebar("♡  Data Mahasiswa", buka_form_mahasiswa)
        buat_tombol_sidebar("♡  Data Mata Kuliah", buka_form_mk)
        buat_tombol_sidebar("♡  Jadwal Kuliah", buka_form_jadwal)
        buat_tombol_sidebar("♡  Data KRS", buka_form_krs)
        buat_tombol_sidebar("♡  Pembayaran UKT", buka_form_ukt)

        # Tombol Keluar / Tutup Aplikasi
        tk.Frame(
            sidebar,
            bg="#E9AFC2",
            height=1
        ).pack(fill=tk.X, padx=25, pady=(25, 15))

        tk.Button(
            sidebar,
            text="♡  Keluar",
            font=("Segoe UI", 10, "bold"),
            bg="#8F3E5A",
            fg="white",
            activebackground="#713047",
            activeforeground="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=dashboard.destroy
        ).pack(fill=tk.X, padx=15, pady=5, ipady=9)

        # Area konten utama dashboard
        content = tk.Frame(
            dashboard,
            bg=self.BG_COLOR
        )
        content.grid(row=0, column=1, sticky="nsew", padx=35, pady=30)

        # Header dashboard
        tk.Label(
            content,
            text="Welcome to Your Dashboard  ♡",
            font=("Georgia", 25, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            anchor="w"
        ).pack(fill=tk.X, pady=(5, 8))

        tk.Label(
            content,
            text=f"Halo, {user['nama_dosen']}! Senang melihatmu kembali.",
            font=("Segoe UI", 11),
            bg=self.BG_COLOR,
            fg=self.MUTED_COLOR,
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 25))

        # Banner sambutan dengan nuansa Coquette Pink
        banner = tk.Frame(
            content,
            bg=self.PINK_LIGHT,
            padx=28,
            pady=25
        )
        banner.pack(fill=tk.X, pady=(0, 25))

        tk.Label(
            banner,
            text="୨୧  A Little Pink, A Lot of Productivity  ୨୧",
            font=("Georgia", 18, "bold"),
            bg=self.PINK_LIGHT,
            fg=self.ACCENT_COLOR
        ).pack(anchor="w")

        tk.Label(
            banner,
            text="Kelola informasi akademik dengan mudah melalui menu di bawah ini.",
            font=("Segoe UI", 10),
            bg=self.PINK_LIGHT,
            fg=self.TEXT_COLOR
        ).pack(anchor="w", pady=(8, 0))

        # Judul bagian menu
        tk.Label(
            content,
            text="♡  Academic Management",
            font=("Georgia", 17, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 15))

        # Area kartu menu yang menyesuaikan lebar jendela
        menu_frame = tk.Frame(content, bg=self.BG_COLOR)
        menu_frame.pack(fill=tk.BOTH, expand=True)

        for kolom in range(3):
            menu_frame.grid_columnconfigure(kolom, weight=1, uniform="menu")

        for baris in range(2):
            menu_frame.grid_rowconfigure(baris, weight=1, uniform="menu")

        # Membuat kartu menu dengan warna dan tombol seragam
        def buat_kartu(parent, baris, kolom, ikon, judul, deskripsi, perintah):
            kartu = tk.Frame(
                parent,
                bg=self.BOX_BG,
                highlightbackground=self.BORDER_COLOR,
                highlightthickness=1,
                padx=18,
                pady=18
            )
            kartu.grid(
                row=baris,
                column=kolom,
                sticky="nsew",
                padx=8,
                pady=8
            )

            tk.Label(
                kartu,
                text=ikon,
                font=("Segoe UI", 25),
                bg=self.BOX_BG,
                fg=self.ACCENT_COLOR
            ).pack(anchor="w")

            tk.Label(
                kartu,
                text=judul,
                font=("Segoe UI", 12, "bold"),
                bg=self.BOX_BG,
                fg=self.TEXT_COLOR,
                anchor="w"
            ).pack(anchor="w", pady=(8, 4))

            tk.Label(
                kartu,
                text=deskripsi,
                font=("Segoe UI", 9),
                bg=self.BOX_BG,
                fg=self.MUTED_COLOR,
                anchor="w",
                justify="left",
                wraplength=220
            ).pack(anchor="w", pady=(0, 12))

            tombol = tk.Button(
                kartu,
                text="Buka Menu  ♡",
                font=("Segoe UI", 9, "bold"),
                bg=self.PINK_LIGHT,
                fg=self.ACCENT_COLOR,
                activebackground=self.ACCENT_COLOR,
                activeforeground="white",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=perintah
            )
            tombol.pack(anchor="w", ipadx=8, ipady=5)

            tombol.bind(
                "<Enter>",
                lambda event: tombol.config(
                    bg=self.ACCENT_COLOR, fg="white"
                )
            )
            tombol.bind(
                "<Leave>",
                lambda event: tombol.config(
                    bg=self.PINK_LIGHT, fg=self.ACCENT_COLOR
                )
            )

        buat_kartu(
            menu_frame, 0, 0,
            "♡",
            "Data Dosen",
            "Kelola informasi dosen.",
            buka_form_dosen
        )

        buat_kartu(
            menu_frame, 0, 1,
            "୨୧",
            "Data Mahasiswa",
            "Kelola data mahasiswa.",
            buka_form_mahasiswa
        )

        buat_kartu(
            menu_frame, 0, 2,
            "✿",
            "Mata Kuliah",
            "Kelola informasi mata kuliah.",
            buka_form_mk
        )

        buat_kartu(
            menu_frame, 1, 0,
            "♡",
            "Jadwal Kuliah",
            "Kelola jadwal perkuliahan.",
            buka_form_jadwal
        )

        buat_kartu(
            menu_frame, 1, 1,
            "✧",
            "Data KRS",
            "Kelola kartu rencana studi.",
            buka_form_krs
        )

        buat_kartu(
            menu_frame, 1, 2,
            "₊˚",
            "Pembayaran UKT",
            "Kelola data pembayaran UKT.",
            buka_form_ukt
        )

        # Footer dashboard
        tk.Label(
            content,
            text="Made with ♡  |  SIAKAD Academic System",
            font=("Segoe UI", 9, "italic"),
            bg=self.BG_COLOR,
            fg=self.MUTED_COLOR
        ).pack(pady=(15, 0))

        dashboard.mainloop()

# Titik awal eksekusi program Python (Main Entry Point)
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
