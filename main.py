from watermarker import *
import json
from options_ui import *

IS_DEBUG=False
DEBUG_IMAGE="pexels-uriel-venegas-176524868-15321479.jpg"
DEBUG_TEXT="SAMPLE TEXT"

class AppUI(QMainWindow):
    def __init__(self):
        super(AppUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if IS_DEBUG:
            self.ui.file_name_edit.setText(DEBUG_IMAGE)
            self.ui.text_edit.setText(DEBUG_TEXT)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Debug Run")
        IS_DEBUG=True
    else:
        try:
            file_name = sys.argv[1]
            print("Arguments")
        except IndexError:
            print("No input file, quitting")
            quit(0)

app = QApplication(sys.argv)
window = AppUI()
window.show()

sys.exit(app.exec())

