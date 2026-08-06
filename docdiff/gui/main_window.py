import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFileDialog, QFrame, QCheckBox, 
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDesktopServices

from docdiff.gui.styles import MODERN_STYLE
from docdiff.gui.worker import DiffWorker

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config.json")

class FileDropCard(QFrame):
    """
    Drag and drop file selection card widget.
    """
    def __init__(self, title: str, placeholder: str, parent=None):
        super().__init__(parent)
        self.setObjectName("DropCard")
        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        header_row = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setObjectName("CardTitle")
        
        self.hint_label = QLabel("可拖入 .docx 文件或输入路径")
        self.hint_label.setObjectName("DropHint")

        header_row.addWidget(self.title_label)
        header_row.addStretch()
        header_row.addWidget(self.hint_label)

        input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(placeholder)

        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.setObjectName("BrowseBtn")
        self.browse_btn.setCursor(Qt.PointingHandCursor)

        input_layout.addWidget(self.path_input, 1)
        input_layout.addWidget(self.browse_btn)

        layout.addLayout(header_row)
        layout.addLayout(input_layout)

        self.browse_btn.clicked.connect(self._on_browse)

    def _on_browse(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, f"选择{self.title_label.text()}", "", "Word Document (*.docx)"
        )
        if file_path:
            self.path_input.setText(file_path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith('.docx') for url in urls):
                self.setProperty("dragActive", True)
                self.style().unpolish(self)
                self.style().polish(self)
                event.acceptProposedAction()
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event: QDropEvent):
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith('.docx'):
                self.path_input.setText(file_path)
                event.acceptProposedAction()
                break

    def get_path(self) -> str:
        return self.path_input.text().strip()

    def set_path(self, path: str):
        self.path_input.setText(path)


class DocDiffWindow(QMainWindow):
    """
    Main Application Window for DocDiff.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocDiff - 文档差异标红对比工具")
        # Set aspect ratio w:h = 3:2 (750 x 500)
        self.resize(750, 500)
        self.setMinimumSize(660, 440)
        self.setStyleSheet(MODERN_STYLE)

        self.worker = None

        self._init_ui()
        self._load_config()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(8)

        # 1. Header Frame
        header_frame = QFrame()
        header_frame.setObjectName("HeaderFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 6, 8, 6)
        header_layout.setSpacing(2)

        title = QLabel("DocDiff 文档标红比对")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("智能对比新旧 Word (.docx) 文档，自动将变更内容显式标红导出")
        subtitle.setObjectName("SubtitleLabel")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_frame)

        # 2. File Cards
        self.old_card = FileDropCard("原文件 (Old Document)", "请选择或拖入旧版本 .docx 文件...")
        self.new_card = FileDropCard("新文件 (New Document)", "请选择或拖入新版本 .docx 文件...")
        
        main_layout.addWidget(self.old_card)
        main_layout.addWidget(self.new_card)

        # Auto output generation hook
        self.new_card.path_input.textChanged.connect(self._auto_update_output_path)

        # 3. Output Card
        output_frame = QFrame()
        output_frame.setObjectName("DropCard")
        output_layout = QVBoxLayout(output_frame)
        output_layout.setContentsMargins(12, 8, 12, 8)
        output_layout.setSpacing(4)

        out_header_row = QHBoxLayout()
        out_title = QLabel("输出文件 (Output Document)")
        out_title.setObjectName("CardTitle")
        out_hint = QLabel("默认在原路径生成 _tracked.docx")
        out_hint.setObjectName("DropHint")

        out_header_row.addWidget(out_title)
        out_header_row.addStretch()
        out_header_row.addWidget(out_hint)

        out_input_layout = QHBoxLayout()
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("留空自动生成，或指定输出文件路径...")
        
        self.output_browse_btn = QPushButton("另存为...")
        self.output_browse_btn.setObjectName("BrowseBtn")
        self.output_browse_btn.setCursor(Qt.PointingHandCursor)
        self.output_browse_btn.clicked.connect(self._on_browse_output)

        out_input_layout.addWidget(self.output_input, 1)
        out_input_layout.addWidget(self.output_browse_btn)

        output_layout.addLayout(out_header_row)
        output_layout.addLayout(out_input_layout)

        main_layout.addWidget(output_frame)

        # 4. Options
        options_layout = QHBoxLayout()
        self.show_deletions_cb = QCheckBox("显示删除内容（红色删除线）")
        self.show_deletions_cb.setChecked(True)
        options_layout.addWidget(self.show_deletions_cb)
        options_layout.addStretch()

        main_layout.addLayout(options_layout)

        # 5. Progress and Status
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # Indeterminate mode when running
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("准备就绪")
        self.status_label.setObjectName("SubtitleLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        # 6. Primary Action Button
        self.run_btn = QPushButton("开始比对并标红导出")
        self.run_btn.setObjectName("PrimaryBtn")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.clicked.connect(self._start_diff)
        main_layout.addWidget(self.run_btn)

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("old_path"):
                        self.old_card.set_path(data["old_path"])
                    if data.get("new_path"):
                        self.new_card.set_path(data["new_path"])
                    if data.get("output_path"):
                        self.output_input.setText(data["output_path"])
                    if "show_deletions" in data:
                        self.show_deletions_cb.setChecked(bool(data["show_deletions"]))
            except Exception:
                pass

    def _save_config(self):
        try:
            data = {
                "old_path": self.old_card.get_path(),
                "new_path": self.new_card.get_path(),
                "output_path": self.output_input.text().strip(),
                "show_deletions": self.show_deletions_cb.isChecked()
            }
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _auto_update_output_path(self, new_path: str):
        new_path = new_path.strip()
        if new_path.lower().endswith('.docx'):
            base, ext = os.path.splitext(new_path)
            default_out = f"{base}_tracked{ext}"
            self.output_input.setPlaceholderText(f"默认: {default_out}")

    def _on_browse_output(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "选择输出文件保存路径", "", "Word Document (*.docx)"
        )
        if file_path:
            if not file_path.lower().endswith('.docx'):
                file_path += '.docx'
            self.output_input.setText(file_path)

    def _get_target_output_path(self, new_path: str) -> str:
        custom_out = self.output_input.text().strip()
        if custom_out:
            return custom_out
        base, ext = os.path.splitext(new_path)
        return f"{base}_tracked{ext}"

    def _start_diff(self):
        old_path = self.old_card.get_path()
        new_path = self.new_card.get_path()

        if not old_path or not os.path.exists(old_path):
            QMessageBox.warning(self, "警告", "请正确选择或拖入【原文件】！")
            return

        if not new_path or not os.path.exists(new_path):
            QMessageBox.warning(self, "警告", "请正确选择或拖入【新文件】！")
            return

        output_path = self._get_target_output_path(new_path)

        # Save paths & options to config.json (git ignored)
        self._save_config()

        # Lock UI
        self.run_btn.setEnabled(False)
        self.progress_bar.show()
        self.status_label.setText("正在解析文档并计算差异，请稍候...")

        # Start Worker Thread
        self.worker = DiffWorker(
            old_path=old_path,
            new_path=new_path,
            output_path=output_path,
            show_deletions=self.show_deletions_cb.isChecked()
        )
        self.worker.finished_signal.connect(self._on_diff_success)
        self.worker.error_signal.connect(self._on_diff_error)
        self.worker.start()

    def _on_diff_success(self, output_path: str):
        self.run_btn.setEnabled(True)
        self.progress_bar.hide()
        self.status_label.setText(f"✓ 比对完成！导出文件: {output_path}")

        reply = QMessageBox.information(
            self,
            "成功",
            f"文档差异比对完成！\n\n标红文件已导出至:\n{output_path}\n\n是否立即打开包含该文件的文件夹？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        if reply == QMessageBox.Yes:
            folder_path = os.path.dirname(os.path.abspath(output_path))
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

    def _on_diff_error(self, error_msg: str):
        self.run_btn.setEnabled(True)
        self.progress_bar.hide()
        self.status_label.setText("× 比对失败")
        QMessageBox.critical(self, "错误", f"计算文档差异时发生错误:\n{error_msg}")

