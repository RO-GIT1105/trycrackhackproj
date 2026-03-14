import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QStackedWidget, QPlainTextEdit
)
from PySide6.QtCore import QTimer, Qt, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QKeySequence
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QStackedLayout
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QTimer


from PIL import Image

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
    return os.path.join(BASE_DIR, path)
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
        self.video.play(asset("assets/videos/mission1.mp4"))

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
            next_widget=None
        )


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
        self.mission1 = MissionOneStegoScreen(self)
        self.mission1_outro = MissionOneOutro(self)
        self.complete = MissionCompleteCommon(self)

        self.mission1_to_2_video = Mission1ToMission2Video(self)
        self.mission2_intro = MissionTwoIntro(self)
        self.mission2 = MissionTwoXorScreen(self)

        # ---- MISSION 2 OBJECTS (ADD THIS BLOCK) ----
        self.mission2_intro = MissionTwoIntro(self)
        self.mission2 = MissionTwoXorScreen(self)
        self.mission2_outro = MissionTwoOutro(self)
        # ---- MISSION 3 OBJECTS ----
        self.mission3_intro = MissionThreeIntro(self)
        self.mission3_desc = MissionThreeDescription(self)
        self.mission3 = MissionThreeDNSScreen(self)
        self.mission3_outro = MissionThreeOutro(self)

        

        self.stack.addWidget(self.home)      # index 0
        self.stack.addWidget(self.cutscene)  # index 1
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
            self.main.stack.setCurrentIndex(2)

   

    def start_video(self):
        self.video.play(asset("assets/videos/mission1.mp4"))

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
        self.main.mission1_outro.start_video()
        self.main.stack.setCurrentIndex(3)
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
        self.video.play(asset("assets/videos/mission1.mp4"))

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
        self.video.play(asset("assets/videos/mission1.mp4"))

    def finish(self):
        self.main.stack.setCurrentWidget(self.main.mission2_intro)
        self.main.mission2_intro.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TryCrackHack()
    window.show()
    sys.exit(app.exec()) 