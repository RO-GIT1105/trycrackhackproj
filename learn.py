import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedWidget,
    QPlainTextEdit, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt


class TryCrackHack(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TRYCRACKHACK – John the Ripper")
        self.setFixedSize(1200,700)
        self.setStyleSheet("background:black;")

        self.stack = QStackedWidget()
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)

        # ================= MCQ DATA =================

        self.questions = [

    {"q":"1. What is the primary purpose of John the Ripper (JtR)?",
     "o":[
        "A network vulnerability scanner",
        "A tool for encrypting sensitive files",
        "An open-source password auditing tool",
        "A real-time intrusion detection system",
        "A firewall configuration tool"
     ],
     "a":2},

    {"q":"2. Which command displays cracked passwords?",
     "o":[
        "john --display",
        "john --show",
        "john --view",
        "john --list",
        "john --cracked"
     ],
     "a":1},

    {"q":"3. Where are Linux password hashes stored?",
     "o":[
        "/etc/passwd",
        "/var/log/auth.log",
        "/etc/shadow",
        "/root/hash.txt",
        "/tmp/passwords"
     ],
     "a":2},

    {"q":"4. Which John the Ripper mode tries common password lists?",
     "o":[
        "Incremental Mode",
        "Dictionary Mode",
        "Single Crack Mode",
        "Brute Force Mode",
        "Hybrid Mode"
     ],
     "a":1},

    {"q":"5. Which file usually contains encrypted password hashes in Linux?",
     "o":[
        "/etc/login",
        "/etc/shadow",
        "/etc/users",
        "/etc/passwords",
        "/usr/passwd"
     ],
     "a":1}

]

        self.q_index = 0
        self.score = 0

        self.create_home()
        self.create_theory()
        self.create_mcq()

    # ================= HOME PAGE =================

    def create_home(self):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("TRYCRACKHACK")
        title.setStyleSheet("color:cyan;font-size:48px;font-weight:bold")

        start_btn = QPushButton("JOHN THE RIPPER – LEARNING MODULE")
        start_btn.setFixedHeight(60)
        start_btn.setStyleSheet("""
        QPushButton{
            color:lime;
            border:2px solid lime;
            font-size:20px;
            padding:10px;
        }
        QPushButton:hover{
            background:lime;
            color:black;
        }
        """)

        start_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(start_btn)

        self.stack.addWidget(page)

    # ================= THEORY PAGE =================

    def create_theory(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        text = QPlainTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet(
            "background:black;color:lime;font-family:Consolas;font-size:14px"
        )

        text.setPlainText(self.load_theory())

        layout.addWidget(text)

        bottom = QHBoxLayout()

        mcq_btn = QPushButton("MCQ TEST")
        home_btn = QPushButton("HOME")

        for btn in (mcq_btn,home_btn):
            btn.setStyleSheet("""
            QPushButton{
                color:cyan;
                border:2px solid cyan;
                font-size:16px;
                padding:10px;
            }
            QPushButton:hover{
                background:cyan;
                color:black;
            }
            """)

        mcq_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        bottom.addWidget(mcq_btn)
        bottom.addStretch()
        bottom.addWidget(home_btn)

        layout.addLayout(bottom)

        self.stack.addWidget(page)

    # ================= MCQ PAGE =================

    def create_mcq(self):

        page = QWidget()
        self.mcq_layout = QVBoxLayout(page)

        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("color:cyan;font-size:20px")

        self.mcq_layout.addWidget(self.question_label)

        self.group = QButtonGroup(self)
        self.options = []

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
                border:2px solid cyan;
                border-radius:9px;
                background:black;
            }

            QRadioButton::indicator:checked{
                border:2px solid cyan;
                border-radius:9px;
                background:cyan;
            }
            """)

            self.group.addButton(rb)
            self.options.append(rb)
            self.mcq_layout.addWidget(rb)

        self.next_btn = QPushButton("NEXT")

        self.next_btn.setStyleSheet("""
        QPushButton{
            color:cyan;
            border:2px solid cyan;
            font-size:16px;
            padding:10px;
        }
        QPushButton:hover{
            background:cyan;
            color:black;
        }
        """)

        self.next_btn.clicked.connect(self.next_question)

        self.mcq_layout.addWidget(self.next_btn)

        self.stack.addWidget(page)

        self.load_question()

    # ================= LOAD THEORY =================

    def load_theory(self):

        try:
            base = os.path.dirname(__file__)
            path = os.path.join(base,"theory","theory1.txt")

            with open(path,"r",encoding="utf-8") as f:
                return f.read()

        except:
            return "Theory file not found."

    # ================= LOAD QUESTION =================

    def load_question(self):

        self.group.setExclusive(False)
        for rb in self.options:
            rb.setChecked(False)
        self.group.setExclusive(True)

        if self.q_index >= len(self.questions):
            self.show_result()
            return

        q = self.questions[self.q_index]

        self.question_label.setText(
            f"Question {self.q_index+1}/{len(self.questions)}\n\n{q['q']}"
        )

        for i,opt in enumerate(self.options):
            opt.setText(q["o"][i])

    # ================= NEXT QUESTION =================

    def next_question(self):

        selected = None

        for i,opt in enumerate(self.options):
            if opt.isChecked():
                selected = i

        if selected == self.questions[self.q_index]["a"]:
            self.score += 1

        self.q_index += 1
        self.load_question()

    # ================= RESULT =================

    def show_result(self):

        for i in reversed(range(self.mcq_layout.count())):
            widget = self.mcq_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        result = QLabel(
            f"TEST COMPLETED\n\nScore: {self.score}/{len(self.questions)}"
        )

        result.setAlignment(Qt.AlignCenter)
        result.setStyleSheet("color:lime;font-size:24px")

        home_btn = QPushButton("HOME")
        home_btn.setStyleSheet("color:cyan;border:2px solid cyan;padding:10px")

        home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        self.mcq_layout.addWidget(result)
        self.mcq_layout.addWidget(home_btn)


# ================= RUN =================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = TryCrackHack()
    window.show()

    sys.exit(app.exec())