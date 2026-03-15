import sys
import os
import hashlib
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PIL import Image
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimedia import *
from PySide6.QtCore import QUrl
import os

class VideoPlayerWithSkip(QWidget):
    def __init__(self, on_finish_callback):
        super().__init__()

        self.on_finish_callback = on_finish_callback

        layout = QVBoxLayout(self)

        # Video widget
        self.video = QVideoWidget()
        layout.addWidget(self.video)

        # Bottom bar with skip
        bottom = QHBoxLayout()
        bottom.addStretch()

        self.skip = QPushButton("SKIP ▶")
        self.skip.setStyleSheet("""
            QPushButton {
                color: cyan;
                background: transparent;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: lime;
            }
        """)
        self.skip.clicked.connect(self.finish)

        bottom.addWidget(self.skip)
        layout.addLayout(bottom)

        # Media player
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video)
        self.player.mediaStatusChanged.connect(self.on_status)

    def play(self, path):
        if not os.path.exists(path):
            self.finish()
            return
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()

    def on_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.finish()

    def finish(self):
        self.player.stop()
        if self.on_finish_callback:
            self.on_finish_callback()





# -------------------------------
# PATH HANDLING (VERY IMPORTANT)
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset(path):
    #return os.path.join(BASE_DIR, path)
    return os.path.join(os.getcwd(), path)
# -------------------------------
# REAL STEGANALYSIS ENGINE (LSB)
# -------------------------------

def extract_lsb_text(image_path, channel='b', max_chars=500):
    try:
        img = Image.open(image_path).convert("RGB")
        pixels = list(img.getdata())

        channel_index = {'r': 0, 'g': 1, 'b': 2}[channel]
        bits = []

        for pixel in pixels:
            bits.append(str(pixel[channel_index] & 1))

        binary = ''.join(bits)

        chars = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) < 8:
                break
            value = int(byte, 2)
            if value == 0:
                break
            chars.append(chr(value))
            if len(chars) >= max_chars:
                break

        return ''.join(chars)

    except Exception as e:
        return None

class MissionTwoIntro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setStyleSheet(
            "background:black; color:lime; font-family:Consolas; font-size:16px;"
        )
        layout.addWidget(self.text)

        self.story = (
            "MISSION 2: THE FALSE CIPHER\n\n"
            "An encrypted transmission was intercepted.\n"
            "No tools. No scripts.\n\n"
            "Only logic.\n\n"
            "Cipher XOR Key = Truth.\n\n"
            "Press ENTER to proceed."
        )

        self.index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_text)
        

        self.enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter.activated.connect(self.go_next)

    def start(self):
        self.text.clear()
        self.index = 0
        self.timer.start(30)

    def type_text(self):
        if self.index < len(self.story):
            self.text.insertPlainText(self.story[self.index])
            self.index += 1
        else:
            self.timer.stop()

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.mission2)

class MissionTwoXorScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)

        title = QLabel("MISSION 2 — THE FALSE CIPHER")
        title.setStyleSheet("color: cyan; font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        instructions = QLabel(
            "Key: MOVE\n"
        "ASCII: M=77  O=79  V=86  E=69\n\n"

        "Cipher (HEX):\n"
        "39 3a 22 23 65 39 3f 22 3a 26 2b 38 65 39 22 3f "
        "20 32 25 65 28 2a 3b 20 2c 21 28 20 38 31\n\n"

        "Method:\n"
        "1. Convert HEX byte → Decimal → Binary\n"
        "2. Convert key ASCII → Binary\n"
        "3. XOR both binaries (1⊕1=0, 1⊕0=1)\n"
        "4. Convert result → Decimal → ASCII\n"
        "5. Repeat using key: MOVE MOVE MOVE...\n\n"

        "Rule:\n"
        "Cipher XOR Key = Plaintext\n\n"

        "Final decrypted message:"
        )
        instructions.setStyleSheet("color: lightgray; font-size: 15px;")
        layout.addWidget(instructions)

        self.input = QPlainTextEdit()
        self.input.setFixedHeight(90)
        self.input.setStyleSheet(
            "background:#111; color:lime; font-family:Consolas; font-size:14px;"
        )
        layout.addWidget(self.input)

        self.btn = QPushButton("VERIFY")
        self.btn.setStyleSheet("border:2px solid cyan; color:cyan; padding:8px;")
        self.btn.clicked.connect(self.check)
        layout.addWidget(self.btn)

        self.msg = QLabel("")
        self.msg.setStyleSheet("color:lime; font-size:16px;")
        layout.addWidget(self.msg)

    def check(self):
        if self.input.toPlainText().strip().lower() == "truth travels through movement":
            self.msg.setText("✔ DECRYPTION SUCCESSFUL")
            QTimer.singleShot(1000, self.next)
        else:
            self.msg.setText("✖ Incorrect — redo XOR")

    def next(self):
        #self.main.mission2_outro.start()
        self.main.stack.setCurrentWidget(self.main.mission2_outro)
        self.main.mission2_outro.start()

class MissionTwoOutro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/m2.2.mp4"))

    def finish(self):
        self.main.show_complete_screen(
            mission_id=2,
            next_widget=self.main.mission3_intro

        )





class MissionCompleteCommon(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.mission_id = None
        self.next_widget = None  # <-- changed

        self.setStyleSheet("background:black;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel("")
        self.title.setStyleSheet(
            "color: lime; font-size: 32px; font-weight: bold;"
        )

        self.subtitle = QLabel("Progress saved automatically.")
        self.subtitle.setStyleSheet("color: gray; font-size: 16px;")

        cont_btn = QPushButton("CONTINUE ▶")
        home_btn = QPushButton("HOME ")

        for btn in (cont_btn, home_btn):
            btn.setFixedWidth(220)
            btn.setStyleSheet("""
                QPushButton {
                    background:black;
                    color: cyan;
                    border: 2px solid cyan;
                    font-size: 16px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background: cyan;
                    color: black;
                }
            """)

        cont_btn.clicked.connect(self.continue_story)
        home_btn.clicked.connect(self.go_home)

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addSpacing(30)
        layout.addWidget(cont_btn)
        layout.addWidget(home_btn)

    def configure(self, mission_id, next_widget):
        """Called whenever a mission finishes"""
        self.mission_id = mission_id
        self.next_widget = next_widget
        self.title.setText(f"MISSION {mission_id} COMPLETE")

       
        

    def continue_story(self):
        if self.next_widget:
            self.main.stack.setCurrentWidget(self.next_widget)

            # auto-start cutscenes / intros
            if hasattr(self.next_widget, "start"):
                self.next_widget.start()
            elif hasattr(self.next_widget, "start_video"):
                self.next_widget.start_video()

    def go_home(self):
        self.main.stack.setCurrentWidget(self.main.home)
class MissionThreeIntro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.mission3_desc)
        self.main.mission3_desc.start()
class MissionThreeDescription(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setStyleSheet(
            "background:black; color:lime; font-family:Consolas; font-size:16px;"
        )
        layout.addWidget(self.text)

        self.story = (
            "MISSION 3: DNS WHISPERS\n\n"
            "Massive DNS traffic detected.\n"
            "Attackers are hiding data in subdomains.\n\n"
            "Base64 encoding confirmed.\n\n"
            "Task:\n"
            "• Filter DNS logs\n"
            "• Extract encoded fragments\n"
            "• Decode the hidden message\n\n"
            "Press ENTER to continue."
        )

        self.index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_text)

        self.enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter.activated.connect(self.go_next)

    def start(self):
        self.text.clear()
        self.index = 0
        self.timer.start(30)

    def type_text(self):
        if self.index < len(self.story):
            self.text.insertPlainText(self.story[self.index])
            self.index += 1
        else:
            self.timer.stop()

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.mission3)





import base64
import re
import random

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton
)
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        # import keyword (orange)
        self.import_format = QTextCharFormat()
        self.import_format.setForeground(QColor("orange"))
        # print keyword (pink)
        self.print_format = QTextCharFormat()
        self.print_format.setForeground(QColor("deeppink"))
        # string format (green)
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("green"))

    def highlightBlock(self, text):
        # highlight import
        if "import" in text:
            index = text.find("import")
            self.setFormat(index, len("import"), self.import_format)
        # highlight print
        if "print" in text:
            index = text.find("print")
            self.setFormat(index, len("print"), self.print_format)
        # highlight strings
        import re
        for match in re.finditer(r'(\".*?\"|\'.*?\')', text):
            start, end = match.span()
            self.setFormat(start, end - start, self.string_format)
class PromptHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        if text.startswith(">>>"):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor("deeppink"))
            self.setFormat(0, 3, fmt)

class MissionThreeDNSScreen(QWidget):
    def __init__(self, parent=None):
        self.parent_window = parent
        super().__init__(parent)

        # ================= CREATE WIDGETS =================

        # Instructions (LEFT TOP)
        title = QLabel("MISSION 3 — DNS WHISPERS")
        title.setStyleSheet("color: cyan; font-size: 26px; font-weight: bold;")
        

        instructions = QLabel(
            "\nPART 1-Filter the logs using Wireshark commands.(In the Right)\n\n"
            "You may use the most known commands like:\n\n"
            "ip.addr == <ip address>   (TO FILTER USING IP/SOURCE)\n"
            "tcp.port == 53            (TO FILTER USING PROTOCOL)\n"
            "frame matches \"<text>\"    (TO FILTER USING TEXT/INFO)\n\n"
            "HINT:\n\n"
            "Spectre affirms that dns code filtered can be encrypted using base64\n"
            "Normally Base64 encryption looks like 'aGVsbG8' for word 'hello'\n"
            "Find similar encrypted DNS text and type base64 decryption code using python\n\n"
            "PART 2-PYTHON IDLE(In the Bottom)\n\n\n"
            ">>>Import the module base64\n"
            ">>>Give the DNS text in encoded variable in quotes\n"
            ">>>Let decode = base64.b64decode(encoded).decode()\n"
            ">>>Display decode"
        )

        instructions.setStyleSheet("""
            font-family:Consolas;
            font-size:14px;
            color:white;
        """)
        instructions.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        instructions.setWordWrap(True)

        # Filter box (RIGHT TOP)
        self.filter_box = QLineEdit()
        self.filter_box.setPlaceholderText("tcp.port == 53")
        self.filter_box.setStyleSheet(
            "background:#eaffea;padding:6px;font-family:Consolas;"
        )
        self.filter_box.returnPressed.connect(self.apply_filter)

        # DNS log screen (RIGHT TOP)
        self.dns_view = QTextEdit()
        self.dns_view.setReadOnly(True)
        self.dns_view.setStyleSheet("""
            background:"#b1fe36";   /* greenish yellow */
            color:black;
            font-family:Consolas;
            font-size:12px;
        """)



        # Python section (BOTTOM FULL WIDTH)
        py_label = QLabel("Python IDLE:")
        py_label.setStyleSheet("font-weight:bold;")

        self.python_editor = QPlainTextEdit()
        self.python_editor.setStyleSheet("""
            background:white;
            color:black;
            font-family:Consolas;
            font-size:14px;
        """)
        self.python_editor.setPlainText(">>> ")
        self.python_editor.installEventFilter(self)

        self.highlighter = PythonHighlighter(self.python_editor.document())

        run_btn = QPushButton("RUN PYTHON")
        run_btn.clicked.connect(self.run_python)

        self.output = QLabel("")
        self.output.setStyleSheet("color:green;font-size:15px;")
        self.mission_box = QLabel("")
        self.mission_box.setStyleSheet("color:red;font-weight:bold;")

        self.retype_box = QLineEdit()
        self.retype_box.setPlaceholderText("Retype decoded message here...")
        self.retype_box.returnPressed.connect(self.check_completion)
        self.success_label = QLabel("")
        self.success_label.setStyleSheet("""
            color: green;
            font-size: 16px;
            font-weight: bold;
        """)
        # ================= LAYOUT STRUCTURE =================

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)


        # ---------- TOP HALF ----------
        top_half = QHBoxLayout()

        # Left side (Instructions)
        left_top = QVBoxLayout()
        left_top.setSpacing(5)          # reduce space between title & instructions
        left_top.setContentsMargins(0, 0, 0, 0)  # remove outer padding

        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        left_top.addWidget(title)
        left_top.addWidget(instructions)
        left_top.addStretch(1)  # keeps everything pushed to top

        # Right side (Filter + DNS)
        right_top = QVBoxLayout()
        right_top.addWidget(self.filter_box)
        right_top.addWidget(self.dns_view)

        top_half.addLayout(left_top, 1)
        top_half.addLayout(right_top, 1)

        main_layout.addLayout(top_half, 1)

        # ---------- BOTTOM HALF ----------
        bottom_half = QVBoxLayout()
        bottom_half.addWidget(py_label)
        bottom_half.addWidget(self.python_editor)
        bottom_half.addWidget(run_btn)
        bottom_half.addWidget(self.output)
        bottom_half.addWidget(self.mission_box)
        bottom_half.addWidget(self.retype_box)
        bottom_half.addWidget(self.success_label)
        main_layout.addLayout(bottom_half, 1)

        main_layout.setStretch(0, 2)
        main_layout.setStretch(1, 1)

        # Load logs
        self.load_logs()

    # ==================================================
    # LOAD REALISTIC MIXED LOGS
    # ==================================================
    def load_logs(self):
        self.all_logs = []

        header = f"{'No.':<6}{'Time':<10}{'Source':<17}{'Destination':<17}{'Protocol':<10}{'Length':<8}Info"
        self.all_logs.append(header)

        packet_no = 1

        # Base64 chunks of: the voice will lie
        b64_chunks = ["dGhl", "IHZv", "aWNl", "IHdp", "bGwg", "bGll"]

        for i in range(70):

            time_val = f"{random.uniform(0.100000,5.900000):.6f}"

            # Insert DNS exfiltration at random spaced intervals
            if i in [5, 14, 23, 37, 49, 62]:
                chunk = b64_chunks.pop(0)
                log = f"{packet_no:<6}{time_val:<10}{'10.0.0.1':<17}{'8.8.8.8':<17}{'DNS':<10}{'92':<8}Standard query A {chunk}.example.com"

            else:
                protocol = random.choice(["TCP", "UDP", "TLS", "ICMP"])
                src = f"192.168.{random.randint(1,5)}.{random.randint(2,200)}"
                dst = f"172.217.{random.randint(1,50)}.{random.randint(1,200)}"
                length = random.randint(54, 1500)

                if protocol == "TCP":
                    info = "HTTP GET /index.html"
                elif protocol == "TLS":
                    info = "Client Hello"
                elif protocol == "UDP":
                    info = "QUIC Stream Data"
                else:
                    info = "Echo (ping) request"

                log = f"{packet_no:<6}{time_val:<10}{src:<17}{dst:<17}{protocol:<10}{str(length):<8}{info}"

            self.all_logs.append(log)
            packet_no += 1

        self.dns_view.setText("\n".join(self.all_logs))
    def eventFilter(self, obj, event):
        if obj == self.python_editor and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.execute_current_line()
                return True
        return super().eventFilter(obj, event)
    def execute_current_line(self):
        import sys
        import io

        text = self.python_editor.toPlainText()
        lines = text.split("\n")
        last_line = lines[-1]

        if not last_line.startswith(">>> "):
            return

        command = last_line[4:].strip()

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            try:
                result = eval(command, globals(), globals())
                if result is not None:
                    print(result)
            except SyntaxError:
                exec(command, globals(), globals())

            output = sys.stdout.getvalue().strip()

            if output:
                self.python_editor.appendPlainText(output)

                if output.lower() == "the voice will lie":

                    # Show success outside Python IDLE
                    self.success_label.setText("Base64 Decryption Successful")

                    # Delay transition
                    QTimer.singleShot(2000, self.go_to_outro)


        except Exception as e:
            self.python_editor.appendPlainText(f"Error: {e}")

        finally:
            sys.stdout = old_stdout

        self.python_editor.appendPlainText(">>> ")
    def go_to_outro(self):
        if self.parent_window:
            self.parent_window.stack.setCurrentIndex(
                self.parent_window.stack.indexOf(
                    self.parent_window.mission3_outro
                )
            )

    # ==================================================
    # FILTER WITH FULL WIDTH GREEN HIGHLIGHT
    # ==================================================
    def apply_filter(self):
        import re

        expr = self.filter_box.text().strip()
        doc = self.dns_view.document()

        # ---------------- RESET ALL FORMATTING ----------------
        block = doc.firstBlock()
        while block.isValid():
            c = QTextCursor(block)
            c.select(QTextCursor.BlockUnderCursor)
            c.setCharFormat(QTextCharFormat())
            block = block.next()

        if not expr:
            return

        # ---------------- VALID COMMAND CHECK ----------------
        valid = False

        if expr.startswith("ip.addr"):
            valid = True
        elif expr.startswith("tcp.port"):
            valid = True
        elif expr.startswith("frame matches"):
            valid = True

        if not valid:
            QMessageBox.warning(self, "Filter Error", "Wrong Command")
            return

        # ---------------- APPLY FILTER ----------------
        block = doc.firstBlock()
        found_any = False

        while block.isValid():
            text = block.text()
            match = False

            # ---- IP FILTER ----
            if expr.startswith("ip.addr"):
                parts = expr.split("==")
                if len(parts) == 2:
                    ip = parts[1].strip()
                    if ip in text:
                        match = True

            # ---- TCP PORT FILTER ----
            elif expr.startswith("tcp.port"):
                parts = expr.split("==")
                if len(parts) == 2:
                    port = parts[1].strip()
                    if port in text:
                        match = True

            # ---- FRAME MATCHES FILTER ----
            elif expr.startswith("frame matches"):
                m = re.search(r'"([^"]+)"', expr)
                if m:
                    search_text = m.group(1)
                    if search_text in text:
                        match = True

            if match:
                found_any = True
                c = QTextCursor(block)
                c.select(QTextCursor.BlockUnderCursor)

                fmt = QTextCharFormat()
                fmt.setBackground(QColor("#00ff00"))  # highlight green
                fmt.setForeground(QColor("black"))

                c.setCharFormat(fmt)

            block = block.next()

        # If no match found
        if not found_any:
            QMessageBox.information(self, "Filter Result", "No matching logs found.")

    # ==================================================
    # RUN PYTHON
    # ==================================================
    def run_python(self):
        code = self.python_editor.toPlainText()
        local_vars = {}

        try:
            exec(code, {}, local_vars)

            output_text = ""

            # If print used
            import re
            prints = re.findall(r'print\((.*?)\)', code)

            for p in prints:
                p = p.strip()

                # If string
                if (p.startswith('"') and p.endswith('"')) or \
                (p.startswith("'") and p.endswith("'")):
                    output_text += p[1:-1] + "\n"

                # If variable
                elif p in local_vars:
                    output_text += str(local_vars[p]) + "\n"

                else:
                    output_text += "RuntimeError: Undefined variable\n"

            self.output.setText(output_text.strip())

            # If decoded correct message
            if "the voice will lie" in output_text.lower():
                self.mission_box.setText(
                    "Message correct! Retype the decoded message exactly below to complete mission."
                )
            else:
                self.mission_box.setText("")

        except SyntaxError:
            self.output.setText("SyntaxError: Invalid syntax")

        except Exception as e:
            self.output.setText(f"RuntimeError: {str(e)}")
    def check_completion(self):
        if self.retype_box.text().strip().lower() == "the voice will lie":
            self.mission_box.setText("MISSION COMPLETE")
            self.mission_box.setStyleSheet("color:green;font-size:18px;font-weight:bold;")

class MissionThreeOutro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.done
        )
        layout.addWidget(self.video)

    def showEvent(self, event):
        super().showEvent(event)
        self.start()

    def start(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

    def done(self):
        self.main.show_complete_screen(
            mission_id=3,
            next_widget=self.main.mission4_intro
        )
class MissionFourIntro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.mission4_desc)
        self.main.mission4_desc.start()
class MissionFourDescription(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setStyleSheet(
            "background:black; color:lime; font-family:Consolas; font-size:16px;"
        )
        layout.addWidget(self.text)

        self.story = (
            "MISSION 4: DISTORTED TRUTH\n\n"
            "An intercepted audio transmission was recovered.\n"
            "The signal is corrupted with noise and frequency distortion.\n\n"
            "Intel suspects a hidden voice message.\n\n"
            "Your task:\n"
            "• Analyze the waveform\n"
            "• Adjust signal parameters\n"
            "• Reveal the hidden voice\n\n"
            "Press ENTER to begin audio lab."
        )

        self.index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_text)

        self.enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter.activated.connect(self.go_next)

    def start(self):
        self.text.clear()
        self.index = 0
        self.timer.start(30)

    def type_text(self):
        if self.index < len(self.story):
            self.text.insertPlainText(self.story[self.index])
            self.index += 1
        else:
            self.timer.stop()

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.mission4)
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QProgressBar, QFrame
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QFont

class MissionFourAudio(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background-color: black;")

        # 🎯 EXACT TARGET VALUES
        self.correct_values = {
            "Frequency": 70,
            "Contrast": 20,
            "Gain": 40,
            "Noise": 0
        }

        self.completed = False

        layout = QVBoxLayout(self)

        # ===== TITLE =====
        title = QLabel("MISSION 4 — AUDIO STEGANALYSIS LAB")
        title.setStyleSheet("color: cyan; font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # ===== AUDIO PLAYER =====
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)

        self.play_btn = QPushButton("▶ INTERCEPTED TRANSMISSION")
        self.play_btn.setStyleSheet("""
            QPushButton {
                background:black;
                color:lime;
                border:2px solid lime;
                padding:10px;
                font-size:16px;
            }
            QPushButton:hover {
                background:lime;
                color:black;
            }
        """)
        self.play_btn.clicked.connect(self.play_audio)
        layout.addWidget(self.play_btn)
        

        # ===== FAKE WAVE PANEL =====
        # ===== FAKE WAVE PANEL =====
        self.wave_panel = QFrame()
        self.wave_panel.setStyleSheet("""
            background-color: #111;
            border: 2px solid cyan;
        """)
        self.wave_panel.setFixedHeight(120)

        wave_layout = QVBoxLayout(self.wave_panel)

        self.wave_label = QLabel("")  # initially empty
        self.wave_label.setAlignment(Qt.AlignCenter)
        self.wave_label.setStyleSheet("""
            color: lime;
            font-size: 22px;
            font-weight: bold;
        """)

        wave_layout.addWidget(self.wave_label)

        layout.addWidget(self.wave_panel)

        # ===== SIGNAL QUALITY BAR =====
        self.quality = QProgressBar()
        self.quality.setRange(0, 100)
        self.quality.setValue(0)
        self.quality.setTextVisible(True)
        self.quality.setFormat("%p%")
        self.quality.setStyleSheet("""
            QProgressBar {
                border: 2px solid cyan;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: lime;
            }
        """)
        layout.addWidget(QLabel("Signal Integrity"))
        layout.addWidget(self.quality)

        # ===== SLIDERS =====
                
        self.sliders = {}
        self.value_labels = {}

        for name in self.correct_values:
            row = QHBoxLayout()
            label = QLabel(name)
            label.setStyleSheet("color: white;")
            label.setFixedWidth(140)

            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 100)
            slider.setStyleSheet("background:#222;")
            slider.valueChanged.connect(self.update_signal)

            value_label = QLabel("0")
            value_label.setStyleSheet("color: cyan; font-weight: bold;")
            value_label.setFixedWidth(40)

            row.addWidget(label)
            row.addWidget(slider)
            row.addWidget(value_label)

            layout.addLayout(row)

            self.sliders[name] = slider
            self.value_labels[name] = value_label

        # ===== STATUS =====
        self.status = QLabel("Adjust parameters to stabilize corrupted audio...")
        self.status.setStyleSheet("color: gray; font-size:15px;")
        layout.addWidget(self.status)

    # =====================================
    # PLAY DISTORTED AUDIO
    # =====================================
    def play_audio(self):
        if not self.completed:
            self.player.setSource(QUrl.fromLocalFile(asset("audio/distorted.wav")))
        else:
            self.player.setSource(QUrl.fromLocalFile(asset("audio/cleanform.wav")))
        self.player.play()

    # =====================================
    # CALCULATE SMOOTH PROGRESS
    # =====================================
    def update_signal(self):
        if self.completed:
            return

        total_difference = 0
        max_difference = 400  # 4 sliders × max 100 difference

        for key in self.correct_values:
            value = self.sliders[key].value()
            self.value_labels[key].setText(str(value))  # Update number display

            diff = abs(value - self.correct_values[key])
            total_difference += diff

        score = max(0, 100 - int((total_difference / max_difference) * 100))
        self.quality.setValue(score)

        if score >= 100:
            self.decode_message()

    # =====================================
    # SUCCESS TRIGGER
    # =====================================
    def decode_message(self):
        if self.completed:
            return

        self.completed = True

        self.player.stop()
        self.player.setSource(QUrl.fromLocalFile(asset("audio/cleanform.wav")))
        self.player.play()

        # Progress bar text change
        self.quality.setValue(100)
        self.quality.setFormat("100%")

        # Show message inside box below button
        self.wave_label.setText("TRUST THE MALWARE")

        self.status.setText("VOICE RECONSTRUCTED SUCCESSFULLY")
        self.status.setStyleSheet("color: lime; font-size:18px; font-weight:bold;")

        QTimer.singleShot(4000, self.go_outro)

    # =====================================
    # NEXT SCREEN
    # =====================================
    def go_outro(self):
        self.main.stack.setCurrentWidget(self.main.mission4_outro)
        self.main.mission4_outro.start()

class MissionFourOutro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.show_complete_screen(
            mission_id=4,
            next_widget=self.main.mission5_intro
        )
# ==========================================
# MISSION 5 INTRO
# ==========================================

class MissionFiveIntro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.mission5_desc)
        self.main.mission5_desc.start()


# ==========================================
# MISSION 5 DESCRIPTION
# ==========================================

class MissionFiveDescription(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setStyleSheet(
            "background:black; color:lime; font-family:Consolas; font-size:16px;"
        )
        layout.addWidget(self.text)

        self.story = (
            "MISSION 5: MALWARE MIRROR\n\n"
            "Multiple executable files recovered.\n"
            "Each file simulates a known malware behavior.\n\n"
            "Identify the attack type correctly.\n"
            "Adjust the environment.\n\n"
            "If all configurations are correct,\n"
            "the final file will execute.\n\n"
            "Press ENTER to continue."
        )

        self.index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_text)

        self.enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter.activated.connect(self.go_next)

    def start(self):
        self.text.clear()
        self.index = 0
        self.timer.start(30)

    def type_text(self):
        if self.index < len(self.story):
            self.text.insertPlainText(self.story[self.index])
            self.index += 1
        else:
            self.timer.stop()

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.mission5_game)
# ==========================================
# MISSION 5 GAME
# ==========================================


class MissionFiveGame(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:black;")
        self.setMinimumSize(900, 600)
        self.camera_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.camera_player.setAudioOutput(self.audio_output)

        file_path = os.path.abspath("audio/camera.wav")
        self.camera_player.setSource(QUrl.fromLocalFile(file_path))
        self.correct = {
            "systemconfig.exe": "Denial of Service",
            "secureaccess.exe": "Brute Force",
            "camerapatchdriver.exe": "Trojan",
            "windowspatch.exe": "Rootkit"
        }

        self.answers = {}

        main_layout = QVBoxLayout(self)

        # ---------------- TITLE (LEFT CORNER) ----------------
        title = QLabel("MISSION 5 — MALWARE MIRROR")
        title.setStyleSheet("color:cyan; font-size:22px; font-weight:bold;")
        title.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title)

        # ---------------- FUNNY INSTRUCTION ----------------
        instruction = QLabel(
            "Experience each malware attack. Name it correctly. "
            "Don't panic — your system probably survives... probably.\n"
            "To adjust environment find right answers for all malware simulation mcqs"
        )
        instruction.setStyleSheet("color:white; font-size:14px;")
        instruction.setWordWrap(True)
        main_layout.addWidget(instruction)

        main_layout.addSpacing(30)

        # ---------------- CENTERED BUTTON CONTAINER ----------------
        self.center_container = QVBoxLayout()
        self.center_container.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(self.center_container)

        self.create_buttons()

        main_layout.addSpacing(40)

        # ---------------- MCQ AREA (FIXED BELOW BUTTONS) ----------------
        self.mcq_widget = QWidget()
        self.mcq_layout = QVBoxLayout(self.mcq_widget)
        self.mcq_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.mcq_widget)

    # DIALOGUE BOX STYLE
    def styled_message_box(self, title, message, text_color="black", icon_type="info"):
            msg = QMessageBox(self)
            msg.setWindowTitle(title)
            msg.setText(message)

            # This triggers the built-in system sound
            if icon_type == "error":
                msg.setIcon(QMessageBox.Critical)
            elif icon_type == "warning":
                msg.setIcon(QMessageBox.Warning)
            else:
                msg.setIcon(QMessageBox.Information)

            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QLabel {
                    color: black;
                    font-size: 14px;
                    background-color: white;
                }
                QPushButton {
                    background-color: white;
                    color: black;
                    padding: 5px 15px;
                }
            """)

            msg.show()
    # --------------------------------------------------
    # CREATE BUTTONS (FIXED POSITION)
    # --------------------------------------------------

    def create_buttons(self):

        files = [
            "systemconfig.exe",
            "secureaccess.exe",
            "camerapatchdriver.exe",
            "windowspatch.exe"
        ]

        for f in files:
            btn = QPushButton(f)
            btn.setFixedWidth(300)
            btn.setStyleSheet(
                "background:black;color:lime;border:2px solid lime;padding:10px;"
            )
            btn.clicked.connect(lambda checked, name=f: self.handle_file(name))
            self.center_container.addWidget(btn)

        run_btn = QPushButton("RUN MALWARE")
        run_btn.setFixedWidth(300)
        run_btn.setStyleSheet(
            "background:black;color:cyan;border:2px solid cyan;padding:12px;font-weight:bold;"
        )
        run_btn.clicked.connect(self.run_malware)
        self.center_container.addWidget(run_btn)

    # --------------------------------------------------
    # HANDLE FILE CLICK
    # --------------------------------------------------

    def handle_file(self, name):

        self.clear_mcq()

        if name == "systemconfig.exe":
            self.flash_and_blackout(5000, lambda: self.show_question(
                name,
                ["Phishing", "SQL Injection", "Denial of Service", "XSS"]
            ))

        elif name == "secureaccess.exe":
            self.spawn_access_denied(20)
            QTimer.singleShot(2000, lambda: self.show_question(
                name,
                ["DNS Spoofing", "Brute Force", "ARP Poisoning", "Worm"]
            ))

        elif name == "camerapatchdriver.exe":
            self.camera_player.stop()
            self.camera_player.play()
            self.flash_screen(200)
            QTimer.singleShot(800, lambda: self.show_question(
                name,
                ["Ransomware", "Spyware", "Trojan", "Keylogger"]
            ))

        elif name == "windowspatch.exe":
            self.fake_progress_bar(lambda: self.no_results_box(name))

    # --------------------------------------------------
    # MALWARE SIMULATIONS
    # --------------------------------------------------

    def flash_and_blackout(self, duration, callback):
        overlay = QWidget(self.window())
        overlay.setGeometry(self.window().rect())
        overlay.setStyleSheet("background:white;")
        overlay.show()

        QTimer.singleShot(300, lambda: overlay.setStyleSheet("background:black;"))
        QTimer.singleShot(duration, lambda: (overlay.deleteLater(), callback()))

    def flash_screen(self, duration):
        overlay = QWidget(self.window())
        overlay.setGeometry(self.window().rect())
        overlay.setStyleSheet("background:white;")
        overlay.show()
        QTimer.singleShot(duration, overlay.deleteLater)

    def spawn_access_denied(self, count):
        for i in range(count):
            QTimer.singleShot(i * 80, self.create_popup)

    def scary_screen(self):
        print("SCARY TRIGGERED")
        self.overlay = QWidget(self.main)
        self.overlay.setGeometry(self.window().rect())
        self.overlay.setStyleSheet("background-color: black;")
        self.overlay.show()
        self.overlay.raise_()
        self.scary_label = QLabel("", self.overlay)
        self.scary_label.setAlignment(Qt.AlignCenter)
        self.scary_label.setStyleSheet("""
            color: white;
            font-size: 48px;
            font-weight: bold;
        """)
        self.scary_label.setGeometry(0, 0, self.overlay.width(), self.overlay.height())

        # Typing setup
        self.full_text = "WHO IS WATCHING??"
        self.current_index = 0

        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.type_writer_effect)
        self.typing_timer.start(120)   # typing speed (lower = faster)

    def start_outro(self):
        self.overlay.deleteLater()
        # create outro if not already created
        if not hasattr(self.main, "mission5_outro"):
            self.main.mission5_outro = MissionFiveOutro(self.main)
            self.main.stack.addWidget(self.main.mission5_outro)
        # switch to outro screen properly
        self.main.stack.setCurrentWidget(self.main.mission5_outro)
        self.main.mission5_outro.start()
            
    def type_writer_effect(self):
        if self.current_index < len(self.full_text):
            self.scary_label.setText(
                self.scary_label.text() + self.full_text[self.current_index]
            )
            self.current_index += 1
        else:
            self.typing_timer.stop()

            # 5 second pause
            QTimer.singleShot(5000, self.start_outro)

    def create_popup(self):
        popup = QMessageBox(self.window())
        popup.setWindowTitle("ACCESS DENIED")
        popup.setText("ACCESS DENIED")
        popup.setIcon(QMessageBox.Critical)

        popup.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 14px;
                background-color: white;
            }
            QPushButton {
                background-color: white;
                color: black;
            }
        """)

        x = random.randint(0, self.width() - 250)
        y = random.randint(0, self.height() - 150)
        popup.move(x, y)

        popup.show()
        QTimer.singleShot(1000, popup.close)
    def fake_progress_bar(self, callback):
        bar = QProgressBar(self)
        bar.setFixedWidth(400)
        bar.setRange(0, 100)
        bar.setStyleSheet("background:black;color:lime;")
        self.mcq_layout.addWidget(bar)

        def update(val=0):
            if val > 100:
                bar.deleteLater()
                callback()
                return
            bar.setValue(val)
            QTimer.singleShot(20, lambda: update(val + 1))

        update()

    # --------------------------------------------------
    # AFTER PROGRESS BAR
    # --------------------------------------------------

    def no_results_box(self, filename):
        self.styled_message_box("Scan Complete", "No results found.", "black",icon_type="error")
        self.show_question(
            filename,
            ["Rootkit", "Backdoor", "Adware", "MITM"]
        )

    # --------------------------------------------------
    # MCQ SYSTEM (FIXED SELECTION)
    # --------------------------------------------------

    def show_question(self, filename, options):

        self.clear_mcq()
        self.current_file = filename

        question = QLabel(f"Identify attack type for: {filename}")
        question.setStyleSheet("color:cyan;font-size:16px;")
        self.mcq_layout.addWidget(question)

        self.radio_group = QButtonGroup(self)

        for opt in options:
            radio = QRadioButton(opt)
            radio.setStyleSheet("""
                QRadioButton {
                    color: white;
                    font-size: 14px;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                    border: 2px solid cyan;
                    border-radius: 9px;
                    background: black;
                }
                QRadioButton::indicator:checked {
                    background: cyan;
                }
            """)
            self.radio_group.addButton(radio)
            self.mcq_layout.addWidget(radio)

        submit_btn = QPushButton("SUBMIT")
        submit_btn.setStyleSheet(
            "background:black;color:cyan;border:2px solid cyan;padding:6px;"
        )
        submit_btn.clicked.connect(self.submit_answer)
        self.mcq_layout.addWidget(submit_btn)

    def submit_answer(self):
        selected = self.radio_group.checkedButton()

        if not selected:
            self.styled_message_box("ERROR", "Select an option first.", icon_type="error")
            return

        self.answers[self.current_file] = selected.text()
        self.styled_message_box("Recorded", "Malware classified.", "black",icon_type="info")
        self.clear_mcq()  

    def make_answer_handler(self, filename, option):
        def handler():
            self.answers[filename] = option
            self.lock_mcq()
        return handler

    def lock_mcq(self):
        for i in range(self.mcq_layout.count()):
            widget = self.mcq_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setDisabled(True)

    def clear_mcq(self):
        while self.mcq_layout.count():
            child = self.mcq_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # --------------------------------------------------
    # RUN MALWARE CHECK
    # --------------------------------------------------

    def run_malware(self):
        if len(self.answers) < 4:
            self.styled_message_box(
                "ERROR",
                "Experience all malware first",
                "red",
                icon_type="error"
            )
            return
        for file in self.correct:
            if self.answers.get(file) != self.correct[file]:
                self.styled_message_box(
                    "RESULT",
                    "Environment not adjusted.",
                    "red",
                    icon_type="error"
                )
                return
        # Success
        self.styled_message_box(
            "SUCCESS",
            "Environment adjusted",
            "black",
            icon_type="info"
        )
        # Trigger scary screen AFTER UI updates
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self.scary_screen)
        
# MISSION 5 OUTRO
# ==========================================

class MissionFiveOutro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.setStyleSheet("background-color: black;")

        # Create label if not created
        if not hasattr(self, "label"):
            self.label = QLabel("", self)
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label.setStyleSheet("""
                color: white;
                font-size: 48px;
                font-weight: bold;
            """)
            self.layout().insertWidget(0, self.label)

        self.video.hide()

        self.text = "WHO IS WATCHING??"
        self.index = 0
        self.label.setText("")

        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.type_writer)
        self.typing_timer.start(120)

    def type_writer(self):
        if self.index < len(self.text):
            self.label.setText(self.label.text() + self.text[self.index])
            self.index += 1
        else:
            self.typing_timer.stop()
            QTimer.singleShot(5000, self.play_video)
            
    def play_video(self):
        self.label.hide()
        self.video.show()
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.show_complete_screen(
            mission_id=5,
            next_widget=self.main.finalmission_intro
        )
class FinalMissionIntro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.finalmission_desc)
        self.main.finalmission_desc.start()
class FinalMissionDescription(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setStyleSheet(
            "background:black; color:lime; font-family:Consolas; font-size:16px;"
        )
        layout.addWidget(self.text)

        self.story = (
            "FINAL MISSION: BLACK CIPHER\n\n"
            "A rogue encryption system has been activated.\n"
            "Multiple cipher layers protect its core.\n\n"
            "If the cipher completes its cycle,\n"
            "all intelligence will be permanently lost.\n\n"
            "Your objective:\n"
            "• Break every cipher layer\n"
            "• Identify hidden cryptographic patterns\n"
            "• Destroy the BLACK CIPHER core\n\n"
            "Press ENTER to begin infiltration."
        )

        self.index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_text)

        self.enter = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter.activated.connect(self.go_next)

    def start(self):
        self.text.clear()
        self.index = 0
        self.timer.start(30)

    def type_text(self):
        if self.index < len(self.story):
            self.text.insertPlainText(self.story[self.index])
            self.index += 1
        else:
            self.timer.stop()

    def go_next(self):
        self.main.stack.setCurrentWidget(self.main.finalmission)
        self.main.finalmission.start()
class FinalMissionBlackCipher(QWidget):

    def __init__(self,main):
        super().__init__()
        self.main = main
        # Window Setup
        self.setWindowTitle("FINAL MISSION - BLACK CIPHER")
        self.setStyleSheet("background-color: black; color: white;")

        self.layer = 1
        self.time_left = 600  # 15 minutes

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout()

        # ===== TITLE ROW =====
        title_row = QHBoxLayout()

        self.title = QLabel("FINAL MISSION - BLACK CIPHER")
        self.title.setFont(QFont("Consolas", 28, QFont.Bold))
        self.title.setStyleSheet("color: cyan;")
        self.title.setAlignment(Qt.AlignLeft)

        self.timer_label = QLabel("Time: 10:00")
        self.timer_label.setFont(QFont("Consolas", 24, QFont.Bold))
        self.timer_label.setStyleSheet("color: red;")
        self.timer_label.setAlignment(Qt.AlignRight)

        title_row.addWidget(self.title)
        title_row.addWidget(self.timer_label)
        main_layout.addLayout(title_row)

        # ===== BODY =====
        body_layout = QHBoxLayout()

        # Sidebar
        self.layer_list = QListWidget()
        self.layer_list.setFont(QFont("Consolas", 20))
        self.layer_list.setFixedWidth(260)
        for i in range(1, 8):
            self.layer_list.addItem(f"Layer {i}")
        body_layout.addWidget(self.layer_list)

        # Right Side Layout
        self.right_layout = QVBoxLayout()

        self.instructions = QTextEdit()
        self.instructions.setReadOnly(True)
        self.instructions.setFont(QFont("Consolas", 20))
        self.instructions.setStyleSheet("background-color: #111; padding:15px;")
        self.right_layout.addWidget(self.instructions)

        # Dynamic Area (used especially for SHA1 layer)
        self.dynamic_area = QVBoxLayout()
        self.right_layout.addLayout(self.dynamic_area)

        # Answer Input
        self.answer_input = QLineEdit()
        self.answer_input.setFont(QFont("Consolas", 22))
        self.answer_input.setStyleSheet("background-color: #222; padding: 12px;")
        self.right_layout.addWidget(self.answer_input)

        # Submit Button
        self.submit_btn = QPushButton("SUBMIT")
        self.submit_btn.setFont(QFont("Consolas", 22, QFont.Bold))
        self.submit_btn.setStyleSheet("background-color: cyan; color: black; padding: 12px;")
        self.submit_btn.clicked.connect(self.check_answer)
        self.right_layout.addWidget(self.submit_btn)

        # Result Label
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Consolas", 22, QFont.Bold))
        self.right_layout.addWidget(self.result_label)

        body_layout.addLayout(self.right_layout)
        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

        # Timer
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Tick sound
        self.tick_sound = QSoundEffect(self)
        self.tick_sound.setSource(QUrl.fromLocalFile(asset("audio/tick.wav")))
        self.tick_sound.setLoopCount(-1)   # infinite loop in PySide6
        self.tick_sound.setVolume(0.4)
        self.tick_sound.setMuted(False)

        self.load_layer()
    def start(self):
        self.reset_mission()
        self.update_timer() 
        self.tick_sound.play()
        self.timer.start(1000)

    # ================= TIMER =================

    def update_timer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"Time: {minutes:02}:{seconds:02}")
        if self.time_left == 60:
            self.tick_sound.setVolume(0.8)
        self.time_left -= 1
        if self.time_left < 0:
                self.timer.stop()
                self.tick_sound.stop()
                self.main.stack.setCurrentWidget(self.main.finalmission_failed)
        
    # ================= CLEAR DYNAMIC AREA =================

    def clear_dynamic_area(self):
        while self.dynamic_area.count():
            widget = self.dynamic_area.takeAt(0).widget()
            if widget:
                widget.deleteLater()

    # ================= LOAD LAYER =================

    def load_layer(self):
        self.layer_list.setCurrentRow(self.layer - 1)
        self.answer_input.clear()
        self.result_label.clear()
        self.clear_dynamic_area()
        self.answer_input.setEnabled(True)

        # -------- LAYER 1 --------
        if self.layer == 1:
            self.instructions.setText("""
LAYER 1 – IP CLASSIFICATION

A: 192.168.0.1
B: 8.8.8.8
C: 127.0.0.1
D: 10.0.0.5
E: 172.16.0.2
F: 1.1.1.1

Private → X
Public → Y
Loopback → Z

Type answer in ABCDEF order.
Example format: XYXY...
""")

        # -------- LAYER 2 --------
        elif self.layer == 2:
            self.instructions.setText("""
LAYER 2 – MODULUS

29 mod 6
45 mod 7
81 mod 9

Example: 1,2,3
""")

        # -------- LAYER 3 --------
        elif self.layer == 3:
            self.instructions.setText("""
LAYER 3 – CAESAR CIPHER

Cipher: PA PZ UV TVYL LHZF
KEY = 7

Shift BACKWARD by 7.
                                      
Method:
Caesar cipher shifts letters by a fixed key.

Encryption:
C = (P + K) mod 26

Decryption:
P = (C - K) mod 26

Where
P = Plain letter
C = Cipher letter
K = Key

Alphabet values:
A=0 B=1 C=2 ... Z=25

Since this is decryption,
SHIFT BACKWARD by 7.

Type result in CAPITALS.
""")                                      


        # -------- LAYER 4 --------
        elif self.layer == 4:
            self.instructions.setText("""
LAYER 4 – AFFINE CIPHER

Cipher Text:
RIWL VELL

Given:
a = 5
b = 8

Encryption Formula:
C = (aP + b) mod 26

Decryption Formula:
P = a⁻¹ (C - b) mod 26

Where
P = Plain letter
C = Cipher letter

Alphabet values:
A=0 B=1 C=2 ... Z=25

Step 1:
Find modular inverse of a

a = 5
a⁻¹ mod 26 = 21

Step 2:
Apply

P = 21 (C - 8) mod 26

Decrypt the message.

Type answer in CAPITALS.
""")
        # -------- LAYER 5 --------
        elif self.layer == 5:
            self.instructions.setText("""
LAYER 5 – NUMBER PATTERN

3, 7, 16, 35, 74, ?

Find next number.
""")

        # -------- LAYER 6 (SHA1 GENERATOR) --------
        elif self.layer == 6:
            self.instructions.setText("""
LAYER 6 – SHA1 IDENTIFICATION

Given Hash:
ac4ec747f6a192492ca97e721641ca107b4f44a2

Modify only the word inside quotes.
Allowed:
cyber
CYBER
cybersecurity
cyber security

Click RUN → Compare hash → Submit correct word.
""")

            self.answer_input.setEnabled(True)

            # Python code preview
            self.sha1_code = QTextEdit()
            self.sha1_code.setReadOnly(True)
            self.sha1_code.setFont(QFont("Consolas", 18))
            self.sha1_code.setStyleSheet("background-color:#111;")
            self.sha1_code.setText("""import hashlib
word = "< write the correct word of hash in below box >"
hash_value = hashlib.sha1(word.encode()).hexdigest()
print(hash_value)
""")
            self.dynamic_area.addWidget(self.sha1_code)

            # Word input
            self.sha1_input = QLineEdit()
            self.sha1_input.setFont(QFont("Consolas", 20))
            self.sha1_input.setStyleSheet("background-color:#222; padding:8px;")
            self.sha1_input.setPlaceholderText("cyber / CYBER / cybersecurity / cyber security")
            self.dynamic_area.addWidget(self.sha1_input)

            # RUN button
            self.run_btn = QPushButton("RUN")
            self.run_btn.setFont(QFont("Consolas", 18, QFont.Bold))
            self.run_btn.setStyleSheet("background-color:orange; color:black; padding:6px;")
            self.run_btn.clicked.connect(self.run_sha1)
            self.dynamic_area.addWidget(self.run_btn)

            # Output
            self.sha1_output = QTextEdit()
            self.sha1_output.setReadOnly(True)
            self.sha1_output.setFont(QFont("Consolas", 18))
            self.sha1_output.setStyleSheet("background-color:#111;")
            self.sha1_output.setFixedHeight(80)
            self.dynamic_area.addWidget(self.sha1_output)

        # -------- LAYER 7 --------
        elif self.layer == 7:
            self.instructions.setText("""
LAYER 7 – ATBASH CIPHER

Cipher Text:
MLD HSZOO GSRH

Atbash uses MIRRORED alphabet.

Mapping:

A ↔ Z
B ↔ Y
C ↔ X
D ↔ W
E ↔ V
F ↔ U
G ↔ T
H ↔ S
I ↔ R
J ↔ Q
K ↔ P
L ↔ O
M ↔ N

Example:
H → S
Z → A

Replace every letter with its mirror.

Type result in CAPITALS.
""")

    # ================= SHA1 RUN =================

    def run_sha1(self):
        word = self.sha1_input.text().strip()

        allowed = ["cyber", "CYBER", "cybersecurity", "cyber security"]

        if word not in allowed:
            self.sha1_output.setText("Allowed only:\ncyber\nCYBER\ncybersecurity\ncyber security")
            return

        hash_value = hashlib.sha1(word.encode()).hexdigest()

        target_hash = "ac4ec747f6a192492ca97e721641ca107b4f44a2"

        if hash_value == target_hash:
            self.sha1_output.setText(hash_value + "\n\nHASH MATCHED")
        else:
            self.sha1_output.setText(hash_value)

    # ================= CHECK ANSWER =================

    def check_answer(self):
        user = self.answer_input.text().strip().upper()

        correct = {
            1: "XYZXXY",
            2: "5,3,0",
            3: "IT IS NO MORE EASY",
            4: "HAIL NULL",
            5: "153",
            6: "CYBER SECURITY",   # Correct word for given SHA1
            7: "NOW SHALL THIS"
        }

        if user == correct[self.layer]:
            self.success()
        else:
            self.fail()

    # ================= SUCCESS =================

    def success(self):

        # Highlight completed layer
        item = self.layer_list.item(self.layer - 1)
        item.setForeground(Qt.green)

        self.result_label.setText(f"Layer {self.layer} Breached")
        self.result_label.setStyleSheet("color: lime;")

        self.layer += 1

        if self.layer > 7:
            self.timer.stop()
            self.tick_sound.stop()
            self.main.stack.setCurrentWidget(self.main.finalmission_destroyed)
            self.main.finalmission_destroyed.start()
        else:
            QTimer.singleShot(1500, self.load_layer)

    # ================= FAIL =================

    def fail(self):
        self.result_label.setText("Wrong Answer (-20 sec)")
        self.result_label.setStyleSheet("color: red;")

        # Reduce 20 seconds
        self.time_left -= 20

        if self.time_left < 0:
            self.time_left = 0

    def reset_mission(self):
        self.timer.stop()
        self.tick_sound.stop()

        self.layer = 1
        self.time_left = 600   # 10 minutes

        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"Time: {minutes:02}:{seconds:02}")

        for i in range(self.layer_list.count()):
            item = self.layer_list.item(i)
            item.setForeground(Qt.white)

        self.load_layer()

class FinalMissionDestroyed(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("background:black;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("BLACK CIPHER DESTROYED")
        label.setStyleSheet("""
            color:white;
            font-size:48px;
            font-weight:bold;
        """)
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)

    def start(self):
        # show for 3 seconds then play outro video
        QTimer.singleShot(3000, self.finish)

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.finalmission_outro)
        self.main.finalmission_outro.start()

class FinalMissionFailed(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("background:black;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("MISSION FAILED")
        title.setStyleSheet(
            "color:red; font-size:32px; font-weight:bold;"
        )

        restart_btn = QPushButton("RESTART")
        home_btn = QPushButton("HOME")

        for btn in (restart_btn, home_btn):
            btn.setFixedWidth(220)
            btn.setStyleSheet("""
                QPushButton {
                    background:black;
                    color: cyan;
                    border: 2px solid cyan;
                    font-size: 16px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background: cyan;
                    color: black;
                }
            """)

        restart_btn.clicked.connect(self.restart)
        home_btn.clicked.connect(self.go_home)

        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(restart_btn)
        layout.addWidget(home_btn)

    def restart(self):
        self.main.finalmission.reset_mission()
        self.main.stack.setCurrentWidget(self.main.finalmission)
        self.main.finalmission.start()

    def go_home(self):
        self.main.stack.setCurrentWidget(self.main.home)

class FinalMissionOutro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )

        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.truth_message)
        self.main.truth_message.start()

class TruthMessageScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("background:black; color:white;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel("")
        self.label.setFont(QFont("Consolas", 28))
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)

        self.text = "In a world of data, truth is the most fragile encryption."
        self.index = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.type_text)

    def start(self):
        self.label.setText("")
        self.index = 0
        self.timer.start(50)

    def type_text(self):
        if self.index < len(self.text):
            self.label.setText(self.label.text() + self.text[self.index])
            self.index += 1
        else:
            self.timer.stop()
            QTimer.singleShot(3000, self.finish)

    def finish(self):
        self.main.show_complete_screen(
            mission_id="FINAL",
            next_widget=self.main.home
        )


class LearningSession(QWidget):

    def __init__(self, main):
        super().__init__()

        self.main = main
        self.module = None
        self.q_index = 0
        self.score = 0

        main_layout = QVBoxLayout(self)

        # TITLE
        title = QLabel("LEARNING SESSION")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:cyan;font-size:40px;font-weight:bold")
        main_layout.addWidget(title)

        # STACK
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # =================================================
        # PAGE 1 : MODULE MENU
        # =================================================

        self.menu_page = QWidget()
        menu_layout = QVBoxLayout(self.menu_page)
        menu_layout.setAlignment(Qt.AlignCenter)

        modules = [
            ("   Password Cracking   ","admin"),
            ("   Network Scanning   ","network"),
            ("   Brute Forcing   ","brute"),
            ("   Phishing   ","phishing"),
            ("   Password generation   ","crunch")
        ]

        for name,key in modules:

            btn = QPushButton(name)
            btn.setFixedHeight(50)

            btn.setStyleSheet("""
            QPushButton{
                background:#111;
                color:lime;
                font-size:18px;
                border:2px solid lime;
            }
            QPushButton:hover{
                background:lime;
                color:black;
            }
            """)

            btn.clicked.connect(lambda _,k=key:self.open_module(k))
            menu_layout.addWidget(btn)

        # TERMINAL BUTTON
        term_btn = QPushButton("TERMINAL")
        term_btn.setFixedHeight(50)

        term_btn.setStyleSheet("""
        QPushButton{
            background:#111;
            color:cyan;
            font-size:18px;
            border:2px solid cyan;
        }
        QPushButton:hover{
            background:cyan;
            color:black;
        }
        """)

        term_btn.clicked.connect(self.open_terminal)

        menu_layout.addWidget(term_btn)

        # BACK TO MAIN WINDOW
        back_main = QPushButton("BACK TO MAIN")
        back_main.setFixedHeight(50)

        back_main.setStyleSheet("""
        QPushButton{
        background:#111;
        color:red;
        font-size:18px;
        border:2px solid red;
        }
        QPushButton:hover{
        background:red;
        color:black;
        }
        """)

        back_main.clicked.connect(self.go_main)

        menu_layout.addWidget(back_main)

        self.stack.addWidget(self.menu_page)
        # =================================================
        # PAGE 2 : THEORY
        # =================================================

        self.theory_page = QWidget()
        theory_layout = QVBoxLayout(self.theory_page)

        self.theory_text = QPlainTextEdit()
        self.theory_text.setReadOnly(True)

        self.theory_text.setStyleSheet(
            "background:black;color:lime;font-family:Consolas;font-size:16px"
        )

        theory_layout.addWidget(self.theory_text)

        # BUTTON BAR
        button_bar = QHBoxLayout()

        self.menu_btn = QPushButton("MENU")
        self.menu_btn.setFixedHeight(40)

        self.mcq_btn = QPushButton("START MCQ")
        self.mcq_btn.setFixedHeight(40)

        self.menu_btn.setStyleSheet("""
        QPushButton{
        background:#111;
        color:orange;
        font-size:16px;
        border:2px solid orange;
        }
        QPushButton:hover{
        background:orange;
        color:black;
        }
        """)

        self.mcq_btn.setStyleSheet("""
        QPushButton{
        background:#111;
        color:lime;
        font-size:16px;
        border:2px solid lime;
        }
        QPushButton:hover{
        background:lime;
        color:black;
        }
        """)

        button_bar.addWidget(self.menu_btn)
        button_bar.addStretch()
        button_bar.addWidget(self.mcq_btn)

        theory_layout.addLayout(button_bar)

        self.menu_btn.clicked.connect(self.go_menu)
        self.mcq_btn.clicked.connect(self.start_mcq)

        self.stack.addWidget(self.theory_page)
        # =================================================
        # PAGE 3 : MCQ
        # =================================================

        self.mcq_page = QWidget()
        mcq_layout = QVBoxLayout(self.mcq_page)

        # QUESTION LABEL
        self.question_label = QLabel("")
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("color:white;font-size:20px")
        mcq_layout.addWidget(self.question_label)

        # RADIO BUTTONS
        self.options_group = QButtonGroup(self)
        self.option_buttons = []

        for i in range(5):
            rb = QRadioButton()
            rb.setStyleSheet("""
                QRadioButton{
                color:lime;
                font-size:16px;
                }

                QRadioButton::indicator{
                width:18px;
                height:18px;
                }

                QRadioButton::indicator:unchecked{
                border:2px solid lime;
                background:black;
                }

                QRadioButton::indicator:checked{
                border:2px solid lime;
                background:lime;
                }
                """)

            self.options_group.addButton(rb, i)
            self.option_buttons.append(rb)

            mcq_layout.addWidget(rb)

        # FEEDBACK
        self.feedback = QLabel("")
        self.feedback.setStyleSheet("color:cyan;font-size:16px")
        mcq_layout.addWidget(self.feedback)

        # BUTTON ROW
        btn_row = QHBoxLayout()

        self.submit_btn = QPushButton("SUBMIT")
        self.submit_btn.setStyleSheet("""
        QPushButton{
        background:#111;
        color:lime;
        font-size:16px;
        border:2px solid lime;
        }
        QPushButton:hover{
        background:lime;
        color:black;
        }
        """)

        self.next_btn = QPushButton("NEXT")
        self.next_btn.setStyleSheet("""
        QPushButton{
        background:#111;
        color:cyan;
        font-size:16px;
        border:2px solid cyan;
        }
        QPushButton:hover{
        background:cyan;
        color:black;
        }
        """)

        self.submit_btn.clicked.connect(self.check_answer)
        self.next_btn.clicked.connect(self.next_question)

        btn_row.addWidget(self.submit_btn)
        btn_row.addWidget(self.next_btn)

        mcq_layout.addLayout(btn_row)

        self.stack.addWidget(self.mcq_page)

        # =================================================
        # PAGE 4 : RESULT
        # =================================================

        self.result_page = QWidget()
        result_layout = QVBoxLayout(self.result_page)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color:cyan;font-size:28px")

        back_btn = QPushButton("MENU")
        back_btn.setFixedHeight(40)

        back_btn.setStyleSheet("""
        QPushButton{
        background:#111;
        color:orange;
        font-size:16px;
        border:2px solid orange;
        }
        QPushButton:hover{
        background:orange;
        color:black;
        }
        """)

        back_btn.clicked.connect(self.go_menu)

        result_layout.addWidget(self.result_label)
        result_layout.addWidget(back_btn)
        self.stack.addWidget(self.result_page)
        # =================================================
        # PAGE 5 : TERMINAL
        # =================================================

        self.terminal_page = QWidget()
        term_layout = QVBoxLayout(self.terminal_page)

        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)

        self.terminal_output.setStyleSheet(
            """
            background:#300030;
            color:white;
            font-family:Consolas;
            font-size:14px;
            """
            )

        self.terminal_input = QLineEdit()
        self.terminal_input.setStyleSheet(
            """
            background:#300030;
            color:white;
            font-family:Consolas;
            font-size:14px;
            """
            )

        self.terminal_input.returnPressed.connect(self.run_command)

        term_layout.addWidget(self.terminal_output)
        term_layout.addWidget(self.terminal_input)

        menu_btn = QPushButton("MENU")
        menu_btn.setFixedHeight(40)

        menu_btn.setStyleSheet("""
        QPushButton{
        background:#111;
        color:orange;
        font-size:16px;
        border:2px solid orange;
        }
        QPushButton:hover{
        background:orange;
        color:black;
        }
        """)

        menu_btn.clicked.connect(self.go_menu)

        term_layout.addWidget(menu_btn)

        self.stack.addWidget(self.terminal_page)

        # =================================================
        # THEORY FILE MAP
        # =================================================

        self.theory_files = {

        "admin":"theory/theory1.txt",
        "network":"theory/theory2.txt",
        "brute":"theory/theory3.txt",
        "phishing":"theory/theory4.txt",
        "crunch":"theory/theory5.txt"

        }

        # =================================================
        # MCQ DATABASE
        # =================================================

        self.mcq_data = {

        "admin":[
        {"q":"Where are Linux password hashes stored?","o":["/etc/passwd","/etc/shadow","/var/pass","/tmp/hash","/root/pass"],"a":1},
        {"q":"Which tool cracks password hashes?","o":["Wireshark","John the Ripper","Nmap","Hydra","Aircrack"],"a":1},
        {"q":"Dictionary attack uses?","o":["random keys","wordlists","rainbow tables","GPU","brute force"],"a":1},
        {"q":"Shadow file stores?","o":["password hashes","logs","network config","keys","tokens"],"a":0},
        {"q":"JtR recommended version?","o":["Lite","Enterprise","Jumbo","Core","Basic"],"a":2}
        ],

        # NMAP
        "network":[
        {"q":"What is the primary purpose of Nmap?","o":["Encrypting files","Network discovery and security auditing","Creating firewalls","Developing websites","Monitoring CPU"],"a":1},
        {"q":"Which Nmap command is used for Ping Scan (Host Discovery)?","o":["nmap -sS <target>","nmap -A <target>","nmap -sn <target>","nmap -sV <target>","nmap -O <target>"],"a":2},
        {"q":"What is the main feature of a Stealth Scan (-sS)?","o":["Completes full TCP handshake","Scans only UDP ports","Does not complete the full TCP handshake","Scans OS only","Captures packets"],"a":2},
        {"q":"Which option is used to detect service version information?","o":["-O","-sV","-sn","-iL","-p"],"a":1},
        {"q":"What does Aggressive Scan (-A) include?","o":["Only OS detection","Only port scanning","OS detection, version detection, script scanning, and traceroute","Only ping scan","Only version detection"],"a":2}
        ],

        # GOBUSTER
        "brute":[
        {"q":"What is the primary purpose of Gobuster?","o":["Encrypt network traffic","Brute-force directories, files, and subdomains on a web server","Monitor CPU usage","Capture network packets","Scan WiFi"],"a":1},
        {"q":"Which Gobuster mode is used to discover hidden directories on a website?","o":["dns","vhost","dir","scan","host"],"a":2},
        {"q":"Which option in Gobuster specifies the target URL?","o":["-w","-u","-t","-o","-d"],"a":1},
        {"q":"Which Gobuster mode is used to enumerate subdomains?","o":["dir","dns","host","scan","file"],"a":1},
        {"q":"Which option is used to provide a wordlist in Gobuster?","o":["-u","-w","-t","-d","-p"],"a":1}
        ],

        # ZPHISHER
        "phishing":[
        {"q":"What is the primary purpose of Zphisher?","o":["Encrypt network communications","Create phishing pages for security awareness demonstrations","Scan open ports on a network","Monitor system processes","Analyze packets"],"a":1},
        {"q":"Zphisher is mainly used to simulate which type of cybersecurity attack?","o":["SQL Injection","Phishing attack","Buffer overflow attack","Denial-of-Service attack","Password cracking"],"a":1},
        {"q":"Which programming language is commonly used in Zphisher templates to process captured data?","o":["Python","Java","PHP","C++","Go"],"a":2},
        {"q":"Which feature of Zphisher helps expose a local phishing server to the internet?","o":["Firewall bypass","Port scanning","Port forwarding/tunneling service","Packet sniffing","VPN"],"a":2},
        {"q":"Zphisher is typically run in which environment?","o":["Windows Command Prompt","Linux terminal environment","Android system settings","Database server console","Browser console"],"a":1}
        ],

        # CRUNCH
        "crunch":[
        {"q":"What is the primary purpose of Crunch?","o":["Generate custom wordlists","Scan open network ports","Capture network packets","Encrypt files","Monitor logs"],"a":0},
        {"q":"Which option in Crunch is used to specify a pattern for generating words?","o":["-p","-t","-w","-u","-s"],"a":1},
        {"q":"Which symbol in Crunch pattern represents lowercase letters?","o":["@ ",",","%","^","*"],"a":0},
        {"q":"Which option in Crunch is used to save the generated wordlist to a file?","o":["-s","-o","-f","-c","-w"],"a":1},
        {"q":"What do the first two parameters in the Crunch command represent?","o":["Minimum and maximum word length","IP address and port","Username and password","Directory and file name","Host and domain"],"a":0}
        ]

        }

    # =================================================
    # FUNCTIONS
    # =================================================

    def open_module(self,module):

        self.module = module

        try:
            with open(self.theory_files[module],"r",encoding="utf-8") as f:
                self.theory_text.setPlainText(f.read())
        except:
            self.theory_text.setPlainText("Theory file missing.")

        self.stack.setCurrentWidget(self.theory_page)

    def start_mcq(self):

        self.questions = self.mcq_data[self.module]

        self.q_index = 0
        self.score = 0

        self.show_question()

        self.stack.setCurrentWidget(self.mcq_page)

    def show_question(self):

        q = self.questions[self.q_index]

        self.question_label.setText(f"Q{self.q_index+1}. {q['q']}")

        self.feedback.setText("")

        for i, opt in enumerate(q["o"]):
            self.option_buttons[i].setText(opt)
            self.option_buttons[i].setChecked(False)

    def check_answer(self):

        selected = self.options_group.checkedId()

        if selected == -1:
            self.feedback.setText("Please select an option")
            return

        correct = self.questions[self.q_index]["a"]
        correct_text = self.questions[self.q_index]["o"][correct]

        if selected == correct:
            self.feedback.setText("✔ Correct")
            self.score += 1
        else:
            self.feedback.setText(f"✘ Wrong | Correct Answer: {correct_text}")    
    def next_question(self):

        self.q_index += 1

        if self.q_index >= len(self.questions):

            self.result_label.setText(
                f"Score: {self.score} / {len(self.questions)}"
            )

            self.stack.setCurrentWidget(self.result_page)

        else:
            self.show_question()

    def go_menu(self):
        self.stack.setCurrentWidget(self.menu_page)
    def go_main(self):
        self.main.show_home()

    # =================================================
    # TERMINAL
    # =================================================

    def open_terminal(self):

        self.terminal_output.clear()
        self.terminal_output.appendPlainText("learningsession@trycrackhack:~$ ")
        self.stack.setCurrentWidget(self.terminal_page)

    def run_command(self):

        cmd = self.terminal_input.text()
        self.terminal_input.clear()

        self.terminal_output.appendPlainText(f"> {cmd}")

        responses = {

        "nmap":"Scanning target...\nOpen ports found.",
        "john":"Running John The Ripper...\nPassword cracked.",
        "hydra":"Brute force started...",
        "zphisher":"Launching phishing toolkit...",
        "crc":"CRC verification completed."

        }

        if cmd in responses:
            self.terminal_output.appendPlainText(responses[cmd])
        else:
            self.terminal_output.appendPlainText("Command not recognized")

        self.terminal_output.appendPlainText("learningsession@trycrackhack:~$ ")
# -------------------------------
# MAIN WINDOW
# -------------------------------

class TryCrackHack(QWidget):
    
    def resume_story(self):
        if self.last_checkpoint is None:
            # Fresh run OR never completed anything
            self.stack.setCurrentWidget(self.cutscene)
            self.cutscene.start_video()

        elif self.last_checkpoint == 1:
            self.complete.configure(
                mission_id=1,
                next_widget=self.mission1_to_2_video
            )
            self.stack.setCurrentWidget(self.complete)

        elif self.last_checkpoint == 2:
            self.complete.configure(
                mission_id=2,
                next_widget=self.home   # later → mission3_intro
            )
            self.stack.setCurrentWidget(self.complete)

    def show_complete_screen(self, mission_id, next_widget):
        self.last_checkpoint = mission_id   # store progress in memory
        self.complete.configure(mission_id, next_widget)
        self.stack.setCurrentWidget(self.complete)
    def show_home(self):
        self.stack.setCurrentWidget(self.home)
    def __init__(self):
        super().__init__()
        self.story_finished = False
        self.last_checkpoint = None

        self.setWindowTitle("TRYCRACKHACK")
        self.showFullScreen()
        self.setStyleSheet("background-color: black;")

        self.stack = QStackedWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        self.home = HomeScreen(self)
        self.cutscene = CutsceneScreen(self)
        self.learning = LearningSession(self)
        self.mission1 = MissionOneStegoScreen(self)
        self.mission1_outro = MissionOneOutro(self)
        self.complete = MissionCompleteCommon(self)

        self.mission1_to_2_video = Mission1ToMission2Video(self)
        
        # ---- MISSION 2 OBJECTS (ADD THIS BLOCK) ----
        self.mission2_intro = MissionTwoIntro(self)
        self.mission2 = MissionTwoXorScreen(self)
        self.mission2_outro = MissionTwoOutro(self)
        # ---- MISSION 3 OBJECTS ----
        self.mission3_intro = MissionThreeIntro(self)
        self.mission3_desc = MissionThreeDescription(self)
        self.mission3 = MissionThreeDNSScreen(self)
        self.mission3_outro = MissionThreeOutro(self)
        # ---- MISSION 4 OBJECTS ----
        self.mission4_intro = MissionFourIntro(self)
        self.mission4_desc = MissionFourDescription(self)
        self.mission4 = MissionFourAudio(self)
        self.mission4_outro = MissionFourOutro(self)
        # ---- MISSION 5 OBJECTS ----
        self.mission5_intro = MissionFiveIntro(self)
        self.mission5_desc = MissionFiveDescription(self)
        self.mission5_game = MissionFiveGame(self)
        self.mission5_outro = MissionFiveOutro(self)
        # ---- MISSION FINAL ----
        self.finalmission_intro = FinalMissionIntro(self)
        self.finalmission_desc = FinalMissionDescription(self)
        self.finalmission = FinalMissionBlackCipher(self)
        self.finalmission_destroyed = FinalMissionDestroyed(self)
        self.finalmission_failed = FinalMissionFailed(self)
        self.finalmission_outro = FinalMissionOutro(self)
        self.truth_message = TruthMessageScreen(self)
        

        self.stack.addWidget(self.home)      # index 0
        self.stack.addWidget(self.cutscene)  # index 1
        self.stack.addWidget(self.learning)
        self.stack.addWidget(self.mission1)  # index 2 
        self.stack.addWidget(self.mission1_outro)   # index 3
        
        self.stack.addWidget(self.mission1_to_2_video)# index 4
        self.stack.addWidget(self.mission2_intro)    # index 5
        self.stack.addWidget(self.mission2)          # index 6
        self.stack.addWidget(self.mission2_outro)    # index 7
        self.stack.addWidget(self.mission3_intro)
        self.stack.addWidget(self.mission3_desc)
        self.stack.addWidget(self.mission3)
        self.stack.addWidget(self.mission3_outro)
        self.stack.addWidget(self.mission4_intro)
        self.stack.addWidget(self.mission4_desc)
        self.stack.addWidget(self.mission4)
        self.stack.addWidget(self.mission4_outro)
        self.stack.addWidget(self.mission5_intro)
        self.stack.addWidget(self.mission5_desc)
        self.stack.addWidget(self.mission5_game)
        self.stack.addWidget(self.mission5_outro)
        self.stack.addWidget(self.finalmission_intro)
        self.stack.addWidget(self.finalmission_desc)
        self.stack.addWidget(self.finalmission)
        self.stack.addWidget(self.finalmission_destroyed)
        self.stack.addWidget(self.finalmission_failed )
        self.stack.addWidget(self.finalmission_outro)
        self.stack.addWidget(self.truth_message)
        

        self.stack.addWidget(self.complete)  # index 8

# -------------------------------
# HOME SCREEN
# -------------------------------

class HomeScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel("TRYCRACKHACK")
        title.setStyleSheet("color: cyan; font-size: 48px; font-weight: bold;")
        subtitle = QLabel("Think. Decode. Survive.")
        subtitle.setStyleSheet("color: gray; font-size: 18px;")
        story_btn = QPushButton("STORY MODE")
        learn_btn = QPushButton("LEARNING SESSION")
        learn_btn.clicked.connect(self.open_learning)
        for btn in (story_btn, learn_btn):
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #111;
                    color: lime;
                    font-size: 18px;
                    border: 2px solid lime;
                }
                QPushButton:hover {
                    background-color: lime;
                    color: black;
                }
            """)
        story_btn.clicked.connect(self.start_story)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(40)
        layout.addWidget(story_btn)
        layout.addWidget(learn_btn)
    def start_story(self):
        self.main.resume_story()
    def open_learning(self):
        self.main.stack.setCurrentWidget(self.main.learning)
    

# -------------------------------
# CUTSCENE SCREEN (VIDEO → TEXT)
# -------------------------------

class CutsceneScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.layout = QVBoxLayout(self)

        # ---- VIDEO ----
        # ---- VIDEO CUTSCENE (COMMON PLAYER WITH SKIP) ----
        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.show_mission_text
        )
        self.layout.addWidget(self.video)

        # ---- TEXT (hidden initially) ----
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setFocusPolicy(Qt.NoFocus) 
        self.text.setStyleSheet(
            "background:black; color:lime; font-family:Consolas; font-size:16px;"
        )
        self.text.hide()
        self.layout.addWidget(self.text)
        self.allow_enter = False

        self.enter_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.enter_shortcut.activated.connect(self.on_enter_pressed)

        self.enter_shortcut2 = QShortcut(QKeySequence(Qt.Key_Enter), self)
        self.enter_shortcut2.activated.connect(self.on_enter_pressed)
    def on_enter_pressed(self):
        if self.allow_enter:
            self.main.stack.setCurrentWidget(self.main.mission1)
   

    def start_video(self):
        self.video.play(asset("assets/videos/m1.1.mp4"))

    def show_mission_text(self):
        self.video.hide()
        self.allow_enter = False
        #self.video_widget.hide()
        #self.skip_btn.hide()
        self.text.clear()
        self.text.show()
        self.setFocus()

        self.story = (
            "MISSION 1: THE SILENT IMAGE\n\n"
            "A journalist was found dead.\n"
            "Minutes before his death, an image was uploaded.\n\n"
            "Intel suspects a hidden message.\n"
            "Your task: Find what the image is hiding.\n\n"
            "Press ENTER to continue..."
        )

        self.index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.type_text)
        self.timer.start(30)

    def type_text(self):
        if self.index < len(self.story):
            self.text.insertPlainText(self.story[self.index])
            self.index += 1
        else:
            self.timer.stop()
            self.allow_enter = True

    

# -------------------------------
# RUN APP
# -------------------------------
class MissionOneStegoScreen(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)

        # ---- TITLE ----
        
        title = QLabel("MISSION 1 — THE SILENT IMAGE")
        title.setStyleSheet("color: cyan; font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        # ---- INSTRUCTIONS ----
        instructions = QLabel(
            "A journalist uploaded an image moments before his death.\n\n"
            " What is Steganography?\n"
            "It is the art of hiding messages inside files like images.\n\n"
            "Your task:\n"
            "• Analyze the image\n"
            "• Use steganography tools\n"
            "• Extract the hidden message\n\n"
            "Hint:\n"
            "Hackers often use a tool called 'zsteg' to analyze PNG images.\n"
            "FILE NAME: image.png\n"
            "Try typing commands in the terminal below."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: lightgray; font-size: 15px;")
        #layout.addWidget(instructions)

        # ---- IMAGE ----
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        image_path = "stock/images/family.png"

        # Check if image exists
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # Scale image to fit nicely
            self.image_label.setPixmap(
                pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        else:
            # Show error message if not found
            self.image_label.setText("❌ family.png not found")
            self.image_label.setStyleSheet("color: red; font-weight: bold;")
        # ---- INSTRUCTIONS + IMAGE SIDE BY SIDE ----
        top_row = QHBoxLayout()

        instructions.setMaximumWidth(520)
        top_row.addWidget(instructions, 2)

        self.image_label.setFixedSize(320, 320)
        top_row.addWidget(self.image_label, 1)

        layout.addLayout(top_row)


        #layout.addWidget(self.image_label)

        # ---- FAKE TERMINAL ----
        self.terminal = QPlainTextEdit()
        self.terminal.setFixedHeight(180)
        self.terminal.setStyleSheet(
            "background-color: #300A24;"
            "color: #F2F2F2;"
            "font-family: Ubuntu Mono, Consolas;"
            "font-size: 14px;"
            "border: 1px solid #5E2750;"
        )

        self.terminal.setPlainText(
            "analyst@synthara:~$ "
        )
        layout.addWidget(self.terminal)
        # ---- FLAG INPUT ----
        self.flag_input = QPlainTextEdit()
        self.flag_input.setPlaceholderText(
            "Paste or type the extracted hidden message here..."
        )
        self.flag_input.setFixedHeight(80)
        self.flag_input.setStyleSheet(
            "background-color: #111;"
            "color: cyan;"
            "font-family: Consolas;"
            "font-size: 14px;"
            "border: 1px solid cyan;"
        )
        #self.flag_input.hide()
        layout.addWidget(self.flag_input)
        self.continue_btn = QPushButton("CONTINUE ▶")
        self.continue_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: lime;
                font-size: 16px;
                border: 2px solid lime;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: lime;
                color: black;
            }
        """)
        self.continue_btn.clicked.connect(self.check_flag)
        layout.addWidget(self.continue_btn)


        # ---- OUTPUT ----
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.hide()
        self.output.setStyleSheet(
            "background:black; color:cyan; font-family:Consolas; font-size:15px;"
        )
        layout.addWidget(self.output)

        # ---- STATE ----
        self.stage = 0  # command stages

        self.terminal.installEventFilter(self)

    # ---- TERMINAL LOGIC ----
    def eventFilter(self, obj, event):
        if obj == self.terminal and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.process_command()
                return True
        return False


    def process_command(self):
        text = self.terminal.toPlainText().strip().lower()

        image_path = "stock/images/image.png"

        # ---- REAL zsteg SIMULATION ----
        if self.stage == 0 and "zsteg image.png" in text:

            self.terminal.appendPlainText("[+] Running zsteg...")

            hidden = extract_lsb_text(image_path, channel='b')

            if hidden and any(c.isprintable() for c in hidden):
                self.terminal.appendPlainText(
                    "imagedata           .. file: PNG image data\n"
                    "b1,r,lsb,xy         .. text: \"random noise\"\n"
                    "b1,g,lsb,xy         .. text: \"nothing useful\"\n"
                    "b1,b,lsb,xy         .. text: FOUND\n"
                    f"b1,b,lsb,xy         .. text: {hidden.strip()}\n"
                    "b4,rgb,lsb,xy       .. text: 'q%'\n"
                    "b4,bgr,lsb,xy       .. text: 'Qt%'\n\n"
                    "analyst@synthara:~$ "
                )


                self.output.show()
                self.output.setPlainText(
                    "PRESS CONTINUE AFTER REWRITING THE MESSAGE"
                )

                self.stage = 2
                self.flag_input.show()
                self.continue_btn.show()

            else:
                self.terminal.appendPlainText(
                    "[-] No hidden data found\n\n"
                    "analyst@synthara:~$ "
                )

        else:
            self.terminal.appendPlainText(
                "\ncommand not recognized\n"
                "Hint: try → zsteg <FILE NAME>\n\n"
                "analyst@synthara:~$ "
            )
    def check_flag(self):
        text = self.flag_input.toPlainText().strip()

        if not text:
            self.output.show()
            self.output.setPlainText("[!] Please type something before continuing.")
            return

        self.output.show()
        self.output.setPlainText("[✓] Input accepted. Proceeding...")
        QTimer.singleShot(800, self.go_to_outro)


    def go_to_outro(self):
        self.main.stack.setCurrentWidget(self.main.mission1_outro)
        self.main.mission1_outro.start_video()
class MissionOneOutro(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start_video(self):
        self.video.play(asset("assets/videos/m1.2.mp4"))

    def finish(self):
        self.main.show_complete_screen(
            mission_id=1,
            next_widget=self.main.mission1_to_2_video  # pass the widget
        )



class Mission1ToMission2Video(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)

        self.video = VideoPlayerWithSkip(
            on_finish_callback=self.finish
        )
        layout.addWidget(self.video)

    def start(self):
        self.video.play(asset("assets/videos/m2.1.mp4"))

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.mission2_intro)
        self.main.mission2_intro.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TryCrackHack()
    window.show()
    sys.exit(app.exec()) 