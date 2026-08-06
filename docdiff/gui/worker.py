from PySide6.QtCore import QThread, Signal
from docdiff.core.engine import DocDiffEngine

class DiffWorker(QThread):
    """
    Worker thread to run document comparison asynchronously without freezing UI.
    """
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, old_path: str, new_path: str, output_path: str, show_deletions: bool = True):
        super().__init__()
        self.old_path = old_path
        self.new_path = new_path
        self.output_path = output_path
        self.show_deletions = show_deletions

    def run(self):
        try:
            engine = DocDiffEngine(
                old_path=self.old_path,
                new_path=self.new_path,
                output_path=self.output_path,
                show_deletions=self.show_deletions
            )
            out_file = engine.execute()
            self.finished_signal.emit(out_file)
        except Exception as e:
            self.error_signal.emit(str(e))
