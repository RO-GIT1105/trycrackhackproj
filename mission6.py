import sys
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QLineEdit,
    QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class FinalMissionBlackCipher(QWidget):

    def __init__(self):
        super().__init__()

        # Window Setup
        self.setWindowTitle("FINAL MISSION - BLACK CIPHER")
        self.setGeometry(100, 50, 1300, 750)
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
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        

        self.load_layer()

    # ================= TIMER =================

    def update_timer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.setText(f"Time: {minutes:02}:{seconds:02}")
        self.time_left -= 1
        if self.time_left < 0:
            self.timer.stop()
            QMessageBox.warning(self, "TIME OVER", "Mission Failed")
            self.close()

    # ================= CLEAR DYNAMIC AREA =================

    def clear_dynamic_area(self):
        while self.dynamic_area.count():
            widget = self.dynamic_area.takeAt(0).widget()
            if widget:
                widget.deleteLater()

    def start(self):
        self.reset_mission()   # reset layers + timer
        self.timer.start(1000)

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
            QMessageBox.information(self, "MISSION COMPLETE", "BLACK CIPHER DESTROYED")
            self.close()
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


# ================= RUN =================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinalMissionBlackCipher()
    window.show()
    sys.exit(app.exec_())