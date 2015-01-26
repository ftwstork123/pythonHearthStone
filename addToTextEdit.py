import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Form(QDialog):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)
		warriorCards = self.getWarriorCards()
		self.lineEdit = QLineEdit(self)
		self.completer = QCompleter(warriorCards, self)
		self.lineEdit.setCompleter(self.completer)		
		self.completer.setCaseSensitivity(Qt.CaseInsensitive)
		grid = QGridLayout() 
		grid.addWidget(self.lineEdit,0,0) 
		#self.removeCardButton = QPushButton('remove card')
		#self.nDiffCards = 0 
		#self.removeCardButton.clicked.connect(lambda : self.removeCard())

		#grid.addWidget(self.removeCard,0,2)
		

		self.setLayout(grid)
		self.getWarriorCards()
	def removeCard(self,cardName):
		print ''
	def getWarriorCards(self):
		with open('cards/neutralList.txt') as f:
			content = f.readlines()
		fileList = [i.replace('\n','').replace('GVGIcon','').replace('CurseofNaxxramasLogo','') for i in content]
		return fileList 
app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()