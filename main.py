from watermarker import *
import json
from options_ui import *
from PySide6.QtWidgets import QColorDialog


IS_DEBUG=False
DEBUG_IMAGE="pexels-uriel-venegas-176524868-15321479.jpg"
DEBUG_TEXT="SAMPLE TEXT"

class AppUI(QMainWindow):
    def __init__(self):
        super(AppUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.options= WatermarkConfig()
        if IS_DEBUG:
            self.ui.file_name_edit.setText(DEBUG_IMAGE)
            self.ui.text_edit.setText(DEBUG_TEXT)
        #signals
        self.ui.button_box.accepted.connect(self._on_accepted)
        self.ui.density_slider.valueChanged.connect(self._on_density_slider_changed)
        self._on_density_slider_changed()
        self.ui.density_edit.editingFinished.connect(self._on_density_text_changed)

        self.ui.color_pick_button.clicked.connect(self._on_pick_color_pressed)

        self.ui.angle_slider.valueChanged.connect(self._on_angle_changed)
        self.ui.angle_edit.editingFinished.connect(self._on_angle_text_changed)
        self._on_angle_changed()

    def _on_angle_text_changed(self):
        self.ui.angle_slider.setValue(int(self.ui.angle_edit.text()))
    def _on_density_text_changed(self):
        self.ui.density_slider.setValue((int(self.ui.density_edit.text())))
    def _on_angle_changed(self):
        self.ui.angle_edit.setText(str(self.ui.angle_slider.value()))
    def _on_pick_color_pressed(self):
        c=QColorDialog.getColor()
        hex_color= c.getRgb()
        r,g,b = hex_color[0],hex_color[1],hex_color[2]
        color_text= str(r).rjust(3,"0")+str(g).rjust(3,"0")+str(b).rjust(3,"0")
        self.ui.color_edit.setText(color_text)
        self.options.FONT_COLOR= (r,g,b)
    def _on_density_slider_changed(self):
        self.ui.density_edit.setText(str(self.ui.density_slider.value()))
    def _on_accepted(self):
        print("Acepted")
        self.options.WATERMARK_OPACITY= float(self.ui.opacity_spinbox.value())
        self.options.FONT_SCALE= int(self.ui.font_scale_spinbox.value())
        self.options.FONT_NAME= self.ui.font_selector.currentFont().family().lower() +".ttf"
        self.options.DENSITY= self.ui.density_slider.value()



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

