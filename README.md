# server_Screan
server control software
# Server Control Panel / Sunucu Kontrol Paneli

## [English]

**Server Control Panel** is a modern, cross-platform application designed to manage Linux servers remotely. It consists of a high-performance **FastAPI** backend and a beautiful **Flet** (Flutter for Python) frontend.

### Features
*   **System Monitoring:** Real-time CPU, RAM, and Disk usage tracking.
*   **Process Manager:** View running processes, search, and kill unwanted tasks.
*   **Service Manager:** Manage systemd services (Start, Stop, Restart).
*   **Remote Terminal:** Execute shell commands directly from the GUI.
*   **Power Controls:** Shutdown or Reboot the server remotely.
*   **Cloudflared Integration:** Built-in tunnel support for remote access without port forwarding.
*   **Customization:** Dark/Light modes, multiple color schemes, and multi-language support (EN, TR, DE, ES, FR).

### Installation & Usage

**Prerequisites:**
*   Python 3.8+
*   `libmpv` (Linux only, for Flet media support)

**1. Create Virtual Environment:**
*   **Linux/macOS:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
*   **Windows:**
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate
    ```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure Server:**
Edit `server/config.yaml` to set your authentication token and Cloudflared settings.

**4. Run Application:**

*   **Linux/macOS:**
    *   Server: `./run_server.sh`
    *   Client: `./run_client.sh`

*   **Windows:**
    *   Server: `run_server.bat`
    *   Client: `run_client.bat`

---

## [Türkçe]

**Sunucu Kontrol Paneli**, Linux sunucularını uzaktan yönetmek için tasarlanmış modern ve platformlar arası bir uygulamadır. Yüksek performanslı **FastAPI** arka ucu ve şık **Flet** (Python için Flutter) ön yüzünden oluşur.

### Özellikler
*   **Sistem İzleme:** Gerçek zamanlı CPU, RAM ve Disk kullanımı takibi.
*   **İşlem Yöneticisi:** Çalışan işlemleri görüntüleyin, arayın ve sonlandırın.
*   **Servis Yöneticisi:** systemd servislerini yönetin (Başlat, Durdur, Yeniden Başlat).
*   **Uzak Terminal:** Kabuk komutlarını doğrudan arayüzden çalıştırın.
*   **Güç Kontrolleri:** Sunucuyu uzaktan kapatın veya yeniden başlatın.
*   **Cloudflared Entegrasyonu:** Port açmaya gerek kalmadan uzaktan erişim için dahili tünel desteği.
*   **Özelleştirme:** Koyu/Açık mod, çoklu renk şemaları ve çoklu dil desteği (TR, EN, DE, ES, FR).

### Kurulum ve Kullanım

**Gereksinimler:**
*   Python 3.8+
*   `libmpv` (Sadece Linux için, Flet medya desteği için gereklidir)

**1. Sanal Ortam (Virtual Env) Kurulumu:**
*   **Linux/macOS:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
*   **Windows:**
    ```cmd
    python -m venv .venv
    .venv\Scripts\activate
    ```

**2. Bağımlılıkları Yükleyin:**
```bash
pip install -r requirements.txt
```

**3. Sunucuyu Yapılandırın:**
`server/config.yaml` dosyasını düzenleyerek yetkilendirme kodunuzu (token) ve Cloudflared ayarlarını yapın.

**4. Uygulamayı Çalıştırın:**

*   **Linux/macOS:**
    *   Sunucu: `./run_server.sh`
    *   İstemci: `./run_client.sh`

*   **Windows:**
    *   Sunucu: `run_server.bat`
    *   İstemci: `run_client.bat`
