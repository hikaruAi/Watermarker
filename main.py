import sys

import watermarker
from watermarker import *
import json
import matplotlib.font_manager
from options_ui import *
from PySide6.QtWidgets import QColorDialog,QMessageBox


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
        else:
            self.ui.file_name_edit.setText(sys.argv[1])
            self.ui.text_edit.setText("YOUR TEXT HERE")
        #signals
        self.ui.button_box.accepted.connect(self._on_accepted)
        self.ui.button_box.rejected.connect(sys.exit)
        ########
        self.ui.opacity_slider.valueChanged.connect(self._on_opacity_slider_changed)
        self.ui.opacity_edit.editingFinished.connect(self._on_opacity_text_changed)
        self._on_opacity_slider_changed()
        ########
        self.ui.density_slider.valueChanged.connect(self._on_density_slider_changed)
        self._on_density_slider_changed()
        self.ui.density_edit.editingFinished.connect(self._on_density_text_changed)
        #########
        self.ui.color_pick_button.clicked.connect(self._on_pick_color_pressed)
        #########
        self.ui.angle_slider.valueChanged.connect(self._on_angle_changed)
        self.ui.angle_edit.editingFinished.connect(self._on_angle_text_changed)
        self._on_angle_changed()
        #######
        self.font_ttf_path = ""
        self.ui.font_selector.currentFontChanged.connect(self._on_font_changed)
        self._on_font_changed()
        #########
        self.ui.write_temp.checkStateChanged.connect(self._on_write_temp_changed)
        self._on_write_temp_changed()
    def _on_write_temp_changed(self):
        watermarker.SAVE_TEMP_IMAGES=self.ui.write_temp.isChecked()
    def _on_font_changed(self):
        self.ui.text_edit.setFont(self.ui.font_selector.currentFont())
        _family=str(self.ui.font_selector.currentFont().family())
        font_prop = matplotlib.font_manager.FontProperties(family=_family)
        self.font_ttf_path = matplotlib.font_manager.findfont(font_prop)
        print(self.font_ttf_path)
    def _on_opacity_text_changed(self):
        v=int(float(self.ui.opacity_edit.text())*100)
        self.ui.opacity_slider.setValue(v)
    def _on_opacity_slider_changed(self):
        self.ui.opacity_edit.setText(str(self.ui.opacity_slider.value()/100))
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
        rgb_as_text= str((r,g,b)) #"color: rgb(255, 0, 0);"
        self.ui.text_edit.setStyleSheet("color: rgb"+ rgb_as_text +";")
        self.options.FONT_COLOR= (r,g,b)
    def _on_density_slider_changed(self):
        self.ui.density_edit.setText(str(self.ui.density_slider.value()))
    def _on_accepted(self):
        print("Acepted")
        self._update_all_options()
        print(self.options)
        message = QMessageBox.information(self, "Proccesing!", "Wait :3")
        watermarker.make_watermark(self.ui.file_name_edit.text(),self.ui.text_edit.text(),options=self.options)
        message_1 = QMessageBox.information(self, "Finished!", "Success")

    def _update_all_options(self):
        self.options.WATERMARK_OPACITY = float(self.ui.opacity_edit.text())
        self.options.FONT_SCALE = int(self.ui.font_scale_spinbox.value())
        self.options.FONT_PATH = self.font_ttf_path
        self.options.DENSITY = self.ui.density_slider.value()
        self.options.WATERMARK_ANGLE = self.ui.angle_slider.value()


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

