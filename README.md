# CyberShell 

CyberShell adalah tool dengan antarmuka GUI dan di Tool tersebut  ada 2 fitur, yang pertama fitur untuk membuat payload reverse shell yang menghasilkan file VBS dan yang ke dua fitur menyuntikkan backdor ke script Python secara otomatis. Dan Tool Dirancang dengan tampilan Dark Neon dan berfokus pada metode stealth & FUD (Fully Undetectable).

---

## Fitur Utama

> VBS Reverse Shell Builder
   - Dukungan 2 metode Obfuscation: `CHR()` dan `Base64`
   - Support ngrok, playit.gg, portmap.io dll
   - File `.vbs` langsung siap pakai

> Python Payload Injector
   - Payload `msfvenom` disisipkan ke file Python target
   - Payload dijalankan dengan threading (background)
   - Output file `_patched.py` tetap menjalankan script asli tanpa error

---

## Cara Penggunaan

```
git clone https://github.com/KaisarYetiandi/CyberShell.git
cd cybershell-builder
```

```
pip3 install -r requirements.txt
python3 CyberShell.py
```

---

## Disclaimer 
Tool ini dibuat hanya untuk edukasi dan pembelajaran saja, Gunakan dengan bijak👍

---

## Contact
Email: `DarknesEmperor@proton.me`
