"""
Modern QSS Styling and Color Tokens for DocDiff
"""

MODERN_STYLE = """
QMainWindow {
    background-color: #0F172A;
}

QWidget {
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    color: #F8FAFC;
}

QFrame#HeaderFrame {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E293B, stop:1 #334155);
    border-bottom: 1px solid #475569;
    border-radius: 8px;
    padding: 8px 12px;
}

QLabel#TitleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #38BDF8;
}

QLabel#SubtitleLabel {
    font-size: 12px;
    color: #94A3B8;
}

QFrame#DropCard {
    background-color: #1E293B;
    border: 1px dashed #475569;
    border-radius: 8px;
    padding: 8px 12px;
}

QFrame#DropCard:hover {
    border-color: #38BDF8;
    background-color: #0F172A;
}

QFrame#DropCard[dragActive="true"] {
    border-color: #22C55E;
    background-color: rgba(34, 197, 94, 0.1);
}

QMessageBox {
    background-color: #1E293B;
}

QMessageBox QLabel {
    color: #F8FAFC;
    font-size: 13px;
}

QMessageBox QPushButton {
    background-color: #334155;
    color: #F8FAFC;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 5px 16px;
    font-weight: 600;
    min-width: 65px;
}

QMessageBox QPushButton:hover {
    background-color: #0284C7;
    border-color: #38BDF8;
}

QLabel#CardTitle {
    font-size: 13px;
    font-weight: 600;
    color: #F1F5F9;
}

QLabel#DropHint {
    font-size: 11px;
    color: #64748B;
}

QLineEdit {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    color: #F8FAFC;
}

QLineEdit:focus {
    border: 1px solid #38BDF8;
}

QPushButton#BrowseBtn {
    background-color: #334155;
    color: #F8FAFC;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#BrowseBtn:hover {
    background-color: #475569;
    border-color: #64748B;
}

QPushButton#PrimaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284C7, stop:1 #2563EB);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#PrimaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #38BDF8, stop:1 #3B82F6);
}

QPushButton#PrimaryBtn:disabled {
    background-color: #334155;
    color: #64748B;
}


QProgressBar {
    border: none;
    background-color: #1E293B;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #38BDF8;
    border-radius: 4px;
}

QCheckBox {
    font-size: 13px;
    color: #CBD5E1;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #475569;
    background-color: #0F172A;
}

QCheckBox::indicator:checked {
    background-color: #0284C7;
    border-color: #38BDF8;
}
"""
