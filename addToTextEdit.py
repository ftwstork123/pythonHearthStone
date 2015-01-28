import sys
from PySide.QtCore import *
from PySide.QtGui import *

class Form(QDialog):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)
		warriorCards = self.getWarriorCards()
		self.nCards = 0
		self.lineEdit = QLineEdit(self)
		self.completer = QCompleter(warriorCards, self)
		self.lineEdit.setCompleter(self.completer)		
		self.completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.grid = QGridLayout() 
		self.grid.addWidget(self.lineEdit,0,0) 
		self.grid.addWidget(QLabel('name of card'),0,1)
		self.grid.addWidget(QLabel('number of times played'),0,2)
		self.lineEdit.returnPressed.connect(lambda : self.addCard(self.lineEdit.text(),warriorCards))
		self.labels = []
		self.counters = []
		self.removeButtons = []
		self.setLayout(self.grid)
	def addCard(self,cardName,cardDeck):
		notInDeck = True
		if cardName not in cardDeck:
			return 
		if self.nCards > 0 :
			for i in range(self.nCards):
				if cardName == self.labels[i].text():
					self.counters[i].setText(str(int(self.counters[i].text())+1))
					notInDeck = False
		if notInDeck : 
			nCard = self.nCards 
			self.labels.append(QLabel(cardName))
			self.counters.append(QLabel('1'))
			self.removeButtons.append(QPushButton('remove'))
			self.grid.addWidget(self.labels[self.nCards],self.nCards+1,1)
			self.grid.addWidget(self.counters[self.nCards],self.nCards+1,2)
			self.grid.addWidget(self.removeButtons[self.nCards],self.nCards+1,3)
			self.removeButtons[self.nCards].clicked.connect(lambda: self.removeCard(nCard))
			self.nCards = self.nCards+1
			self.setLayout(self.grid)
	def removeCard(self,cardName): 
		if int(self.counters[cardName].text()) > 0 : 
			self.counters[cardName].setText(str(int(self.counters[cardName].text()) - 1 ))
	def getWarriorCards(self):
		with open('cards/neutralList.txt') as f:
			content = f.readlines()
		fileList = [i.replace('\n','').replace('GVGIcon','').replace('CurseofNaxxramasLogo','') for i in content]
		return fileList 
app = QApplication(sys.argv)
form = Form()
form.show() 

app.exec_()