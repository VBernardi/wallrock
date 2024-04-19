import sys
import os
import shutil
import ctypes
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QScrollArea, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QFont, QFontMetrics



class LabelImage(QLabel):
    def __init__(self, image_path, main_window):
        super().__init__()

        self.image_path = image_path
        self.main_window = main_window
        self.setPixmap(QPixmap(image_path))

    def mousePressEvent(self, e):
        if e.buttons() == Qt.RightButton:
            self.main_window.update_large_image(self.image_path)
            self.main_window.update_wallpaper(self.image_path)
    
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)

class LabelFolder(QLabel):
    def __init__(self, name, main_window):
        super().__init__(name)

        self.main_window = main_window
        self.name = name

    def mousePressEvent(self, e):
        if self.name == "back":
            self.main_window.back_selected_folder()
        else:
            if e.button() == Qt.LeftButton:
                self.main_window.update_selected_folder(self.name)       

class LabelFolderBack(QLabel):
    def __init__(self, image_path, main_window):
        super().__init__()
        self.name = "back"

        self.image_path = image_path
        self.main_window = main_window
        self.setPixmap(QPixmap(image_path))

    def mousePressEvent(self, e):
        self.main_window.back_selected_folder()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

        self.setWindowTitle("Fond Ecran")
        self.setGeometry(550, 550, 800, 550)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)


        self.layout = QGridLayout(self.central_widget)

        self.image_folder_path = ""
        self.check_image_folder_path()
        if not self.image_folder_path:
            self.select_image_folder()
        self.selected_folder_path = self.image_folder_path

        self.folder_scroll_area = QScrollArea()
        self.folder_scroll_area.setWidgetResizable(True)
        self.folder_scroll_widget = QWidget()
        self.folder_scroll_layout = QGridLayout(self.folder_scroll_widget)
        self.folder_scroll_area.setWidget(self.folder_scroll_widget)
        self.layout.addWidget(self.folder_scroll_area, 0, 0)

        # premier colonne : images scroll
        self.image_scroll_area = QScrollArea()
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area_widget = QWidget()
        self.image_scroll_area_layout = QGridLayout(self.image_scroll_area_widget)
        self.image_scroll_area.setWidget(self.image_scroll_area_widget)
        self.image_scroll_area.setMinimumHeight(400)
        self.layout.addWidget(self.image_scroll_area, 1, 0)  # Utiliser 1 colonne pour la zone de défilement

        # bouton en bas de la colonne 
        self.add_file_button = QPushButton("Ajouter une image", self.central_widget)
        self.add_file_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.add_file_button, 2, 0)  # Positionnement du bouton


        # deuxième colonne : image sélectionnée
        self.selected_image_label = QLabel()
        self.layout.addWidget(self.selected_image_label, 1, 1)

        self.default_image_path = None

        self.display_images()

        self.display_folders()
    

    def check_image_folder_path(self):
        # Vérifie si le chemin du dossier est déjà enregistré dans un fichier ou une base de données
        # Ici, nous supposons que le chemin est stocké dans un fichier texte nommé "image_folder_path.txt"
        if os.path.exists(".image_folder_path.txt"):
            with open(".image_folder_path.txt", "r") as file:
                self.image_folder_path = file.read().strip()

    def select_image_folder(self):
        # Demande à l'utilisateur de sélectionner le dossier d'images
        folder_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier d'images")
        if folder_path:
            self.image_folder_path = folder_path
            # Enregistrer le chemin du dossier dans un fichier ou une base de données pour une utilisation ultérieure
            with open(".image_folder_path.txt", "w") as file:
                file.write(self.image_folder_path)


    def display_images(self, refresh=False):
        image_folder = self.selected_folder_path
        image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        image_files = [f for f in image_files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

        for i, image_file in enumerate(image_files):
            image_path = os.path.join(image_folder, image_file)
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(200, 200, aspectRatioMode=True)
            label = LabelImage(image_path, self)
            label.setPixmap(pixmap)
            self.image_scroll_area_layout.addWidget(label, i, 0)
            if i == 0:  # Garder le chemin de la première image par défaut
                self.default_image_path = image_path

        # affichage image par défaut
        if self.default_image_path and not refresh:
            self.update_large_image(self.default_image_path)

    def update_large_image(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(500, 500, aspectRatioMode=True)
        self.selected_image_label.setPixmap(pixmap)
    
    def update_wallpaper(self, image_path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

    def refresh_images(self):
        # on supprime les anciennes images
        for i in reversed(range(self.image_scroll_area_layout.count())):
            widget = self.image_scroll_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.display_images(refresh=True)

    
    def display_folders(self):
        folder_path = self.selected_folder_path
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

        row = 0
        col = 0
        font = QFont()
        font.setPointSize(12)

        backArrowPath = self.image_folder_path+"/.config/left-arrow.png"
        pixmap = QPixmap(backArrowPath)
        pixmap = pixmap.scaled(30, 30, aspectRatioMode=True)
        folder_back = LabelFolderBack(backArrowPath, self)
        folder_back.setPixmap(pixmap)

        self.folder_scroll_layout.addWidget(folder_back, row, col)
        col += 1

        for i, folder in enumerate(folders):
            if folder != ".config" and folder != "build" and folder != "dist" and folder != "venv" and folder != ".git":
                folder_label = LabelFolder(folder, self)
                folder_label.setFont(font)

                self.folder_scroll_layout.addWidget(folder_label, row, col) # en ligne
                col += 1
                if col == 2:
                    col = 0
                    row += 1
    

    def refresh_folder(self):
        # supprime les anciens dossier
        for i in reversed(range(self.folder_scroll_layout.count())):
            widget = self.folder_scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.display_folders()

    
    def update_selected_folder(self, folder_name):
        self.selected_folder_path = self.selected_folder_path + "/" + folder_name
        # print("selected folder", self.selected_folder_path)
        self.refresh_images()
        self.refresh_folder()
        
    def back_selected_folder(self):
        self.selected_folder_path = "/".join(self.selected_folder_path.split("/")[:-1])
        # print("selec", self.selected_folder_path)
        if self.selected_folder_path != "":
            self.refresh_images()
            self.refresh_folder()
        else:
            self.selected_folder_path = self.image_folder_path
            self.refresh_folder()


    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Sélectionner un fichier à ajouter", "", "Tous les fichiers (*);;Texte (*.txt);;Images (*.png *.jpg)")
        # enregistrement de l'image dans le dossier courant
        if file_path:
            destination_folder = self.selected_folder_path
            shutil.copy(file_path, destination_folder)
            # print(f"Le fichier {file_path} a été ajouté dans {destination_folder}")

            self.refresh_images()


    # DRAG AND DROP
    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        # print("=>", self.folder_scroll_layout)
        # print("pos", pos, "widget", widget, widget.text())

        for n in range(len(self.folder_scroll_layout)):

            w = self.folder_scroll_layout.itemAt(n).widget()
            # print("w", w.text())
            # print("posy", pos.y(), "wy", w.y(), "posx", pos.x(), "wx", w.x())
            # print("posy", pos.y()-30, "wy", w.y()-30, "posx", pos.x()-30, "wx", w.x()-30)
            if w.y()-30 < pos.y()-40 < w.y() and w.x()-30 < pos.x()-40 < w.x():

                if w.name == "back":
                    shutil.move(widget.image_path, "/".join(self.selected_folder_path.split("/")[:-1]))
                    self.refresh_images()
                    break
                else:

                    # self.folder_scroll_layout.addWidget(widget, n-2, 0)
                    # print("file", widget.image_path, "folder", self.selected_folder_path+"/"+w.text())
                    shutil.move(widget.image_path, self.selected_folder_path+"/"+w.text())
                    self.refresh_images()
                    break

        e.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
