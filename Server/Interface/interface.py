import time 
import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QTimer, Qt, QModelIndex, qInstallMessageHandler
from Interface.ui_classes import *
from init_server import initialize_server
from database_management import user_management


# This is to ignore some warnings which were thrown when gui exited and 
# python deleted some assests in wrong order
# Nothing critical :)
def handler(msg_type, msg_log_context, msg_string):
	pass
qInstallMessageHandler(handler)

# This class handles the main window of server
class server_window(QMainWindow):
	def __init__(self, data_changed_flags2, data_to_client):
		super().__init__()
		# Set app icon
		self.setWindowIcon(QIcon('Elements/logo.png'))
		# Set window title
		self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ]')

		# Make  the app run full-screen
		# Initialize status bar (Bottom Bar)
		self.status = self.statusBar()
		self.resize(1024, 768)

		# Timer to update GUI every 1 second
		self.timer = QTimer()
		self.change_flag = True
		self.timer.timeout.connect(self.update_data)
		self.timer.start(1000)
		
		# make data_changed_flag accessible from the class methods
		self.data_changed_flags = data_changed_flags2
		self.data_to_client = data_to_client
		
		###########################################################
		self.db = self.init_qt_database()
		###########################################################
		self.config = initialize_server.read_config()
		# Define Sidebar Buttons and their actions
		button_width = 200
		button_height = 50

		self.button_0 = QPushButton('Accounts', self)
		self.button_0.setFixedSize(button_width, button_height)
		self.button_0.clicked.connect(self.manage_accounts)
		self.button_0.setObjectName("sidebar_button")

		self.button_1 = QPushButton('Submissions', self)
		self.button_1.setFixedSize(button_width, button_height)
		self.button_1.clicked.connect(self.view_submissions)
		self.button_1.setObjectName("sidebar_button")

		self.button_2 = QPushButton('Judges', self)
		self.button_2.setFixedSize(button_width, button_height)
		self.button_2.clicked.connect(self.manage_judges)
		self.button_2.setObjectName("sidebar_button")

		self.button_3 = QPushButton('Clients', self)
		self.button_3.setFixedSize(button_width, button_height)
		self.button_3.clicked.connect(self.manage_clients)
		self.button_3.setObjectName("sidebar_button")

		self.button_4 = QPushButton('Queries', self)
		self.button_4.setFixedSize(button_width, button_height)
		self.button_4.clicked.connect(self.manage_queries)
		self.button_4.setObjectName("sidebar_button")

		self.button_5 = QPushButton('Leaderboard', self)
		self.button_5.setFixedSize(button_width, button_height)
		self.button_5.clicked.connect(self.manage_leaderboard)
		self.button_5.setObjectName("sidebar_button")

		self.button_6 = QPushButton('Problems', self)
		self.button_6.setFixedSize(button_width, button_height)
		self.button_6.clicked.connect(self.manage_problems)
		self.button_6.setObjectName("sidebar_button")

		self.button_7 = QPushButton('Languages', self)
		self.button_7.setFixedSize(button_width, button_height)
		self.button_7.clicked.connect(self.manage_languages)
		self.button_7.setObjectName("sidebar_button")

		self.button_8 = QPushButton('Statistics', self)
		self.button_8.setFixedSize(button_width, button_height)
		self.button_8.clicked.connect(self.show_stats)
		self.button_8.setObjectName("sidebar_button")

		self.button_9 = QPushButton('Settings', self)
		self.button_9.setFixedSize(button_width, button_height)
		self.button_9.clicked.connect(self.contest_settings)
		self.button_9.setObjectName("sidebar_button")

		self.button_10 = QPushButton('Generate Report', self)
		self.button_10.setFixedSize(button_width, button_height)
		self.button_10.clicked.connect(self.generate_report)
		self.button_10.setObjectName("sidebar_button")

		self.button_11 = QPushButton('About', self)
		self.button_11.setFixedSize(button_width, button_height)
		self.button_11.clicked.connect(self.show_about)
		self.button_11.setObjectName("sidebar_button")

		###########################################################

		###########################################################
		# Manage tabs on the right window
		# Each tab is an object returned by the respective function associated with its UI
		# Tab UI are managed by interface_packages/ui_classes.py file 
		self.tab0, self.account_model = ui_widgets.accounts_ui(self)
		self.tab1, self.sub_model = ui_widgets.submissions_ui(self)
		self.tab2 = ui_widgets.judge_ui(self)
		self.tab3, self.client_model = ui_widgets.client_ui(self)
		self.tab4, self.query_model = ui_widgets.query_ui(self)
		self.tab5 = ui_widgets.leaderboard_ui(self)
		self.tab6 = ui_widgets.problem_ui(self)
		self.tab7 = ui_widgets.language_ui(self)
		self.tab8 = ui_widgets.stats_ui(self)
		self.tab9 = ui_widgets.settings_ui(self)
		self.tab10 = ui_widgets.reports_ui(self)
		self.tab11 = ui_widgets.about_us_ui(self)
		
		###########################################################
		
		# Add widgets to our main window
		server_window.init_UI(self)
		return
	

	def init_UI(self):
		self.set_status('SETUP')
		# Define Layout for sidebar
		side_bar_layout = QVBoxLayout()

		# Add buttons to our layout
		side_bar_layout.addWidget(self.button_0)
		side_bar_layout.addWidget(self.button_1)
		side_bar_layout.addWidget(self.button_2)
		side_bar_layout.addWidget(self.button_3)
		side_bar_layout.addWidget(self.button_4)
		side_bar_layout.addWidget(self.button_5)
		side_bar_layout.addWidget(self.button_6)
		side_bar_layout.addWidget(self.button_7)
		side_bar_layout.addWidget(self.button_8)
		side_bar_layout.addWidget(self.button_9)
		side_bar_layout.addWidget(self.button_10)
		side_bar_layout.addWidget(self.button_11)


		# Set stretch and spacing
		side_bar_layout.addStretch(1)
		side_bar_layout.setSpacing(0)

		# Define our sidebar widget and set side_bar_layout to it.
		side_bar_widget = QWidget()
		side_bar_widget.setLayout(side_bar_layout)
		side_bar_widget.setFixedWidth(215)
		side_bar_widget.setObjectName("sidebar")

		#Define our top bar
		logo = QLabel(self)
		logo_image = QPixmap('Elements/bitwise_header.png')
		logo_image2 = logo_image.scaledToWidth(104)
		logo.setPixmap(logo_image2)

		top_bar_layout = QHBoxLayout()
		top_bar_layout.setContentsMargins(15, 5, 20, 0);
		top_bar_layout.addWidget(logo)
		# top_bar_layout.addWidget(start_button)
		# top_bar_layout.addWidget(pause_button)
		# top_bar_layout.addWidget(stop_button)
		top_bar_layout.setStretch(0, 70)
		# top_bar_layout.setStretch(1, 10)
		# top_bar_layout.setStretch(2, 10)
		# top_bar_layout.setStretch(3, 10)

		top_bar_widget = QWidget()
		top_bar_widget.setLayout(top_bar_layout)
		top_bar_widget.setObjectName('top_bar')

		# Define our right side screens corresponding to buttons on the sidebar
		# Basically right screens are tab widgets whose tabs are hidden, 
		# and we map sidebar buttons to each tab switch :)
		# Since sidebars are not natively supported by pyqt5
		self.right_widget = QTabWidget()
		self.right_widget.setObjectName("main_tabs")

		self.right_widget.addTab(self.tab0, '')
		self.right_widget.addTab(self.tab1, '')    # tab names are '' because we don't want them to show up in our screen
		self.right_widget.addTab(self.tab2, '')
		self.right_widget.addTab(self.tab3, '')
		self.right_widget.addTab(self.tab4, '')
		self.right_widget.addTab(self.tab5, '')
		self.right_widget.addTab(self.tab6, '')
		self.right_widget.addTab(self.tab7, '')
		self.right_widget.addTab(self.tab8, '')
		self.right_widget.addTab(self.tab9, '')
		self.right_widget.addTab(self.tab10, '')
		self.right_widget.addTab(self.tab11, '')
		

		# Screen 1 will be our initial screen 
		self.right_widget.setCurrentIndex(9)

		# Define the combined layout for sidebar + right side screens
		main_layout = QHBoxLayout()
		main_layout.addWidget(side_bar_widget)
		main_layout.addWidget(self.right_widget)

		# setstretch( index, stretch_value )
		main_layout.setStretch(0, 0)
		main_layout.setStretch(1, 90)
		# Define our main wideget = sidebar + windows
		main_widget = QWidget()
		main_widget.setObjectName("screen_widget")
		main_widget.setLayout(main_layout)


		#Define top_layout = logo_bar + main_layout
		top_layout = QVBoxLayout()
		top_layout.addWidget(top_bar_widget)
		top_layout.addWidget(main_widget)
		top_layout.setContentsMargins(1, 0, 1, 1)
		top_layout.setStretch(0, 8)
		top_layout.setStretch(1, 100)

		top_widget = QWidget()
		top_widget.setLayout(top_layout)
		top_widget.setObjectName("main_widget")

		# Set top_widget as our central widget
		self.setCentralWidget(top_widget)
		return

	@pyqtSlot()
	def manage_accounts(self):
		self.right_widget.setCurrentIndex(0)

	@pyqtSlot()
	def view_submissions(self):
		self.right_widget.setCurrentIndex(1)

	@pyqtSlot()
	def manage_judges(self):
		self.right_widget.setCurrentIndex(2)

	@pyqtSlot()
	def manage_clients(self):
		self.right_widget.setCurrentIndex(3)

	@pyqtSlot()
	def manage_queries(self):
		self.right_widget.setCurrentIndex(4)

	@pyqtSlot()
	def manage_leaderboard(self):
		self.right_widget.setCurrentIndex(5)

	@pyqtSlot()
	def manage_problems(self):
		self.right_widget.setCurrentIndex(6)

	@pyqtSlot()
	def manage_languages(self):
		self.right_widget.setCurrentIndex(7)

	@pyqtSlot()
	def show_stats(self):
		self.right_widget.setCurrentIndex(8)

	@pyqtSlot()
	def contest_settings(self):
		self.right_widget.setCurrentIndex(9)

	@pyqtSlot()
	def generate_report(self):
		self.right_widget.setCurrentIndex(10)

	@pyqtSlot()
	def show_about(self):
		self.right_widget.setCurrentIndex(11)

	####################################################
	# Functions related to GUI updates
	def update_data(self):
		# If data has changed in submission table
		if self.data_changed_flags[0] == 1:
			self.sub_model.select()
			self.set_flags(0, 0)
		if self.data_changed_flags[1] == 1:
			self.client_model.select()
			self.set_flags(1, 0)
		if self.data_changed_flags[5] == 1:
			self.account_model.select()
			self.set_flags(5, 0)
		if self.data_changed_flags[9] == 1:
			self.query_model.select()
			self.set_flags(9, 0)
		if self.data_changed_flags[10] == 1:
			self.set_status('RUNNING')
			self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ][ RUNNING ]')
		elif self.data_changed_flags[10] == 2:
			self.set_status('STOPPED')
			self.setWindowTitle('BitsOJ v1.0.1 [ SERVER ][ STOPPED ]')
		return

	def send_data_to_client_thread(self, data, extra_data = '02:00'):
		if data == 'START':
			self.data_changed_flags[10] = 1
			message = {
			'Code' : 'START',
			'Time' : extra_data
			}
			message = json.dumps(message)
			self.data_to_client.put(message)
		elif data == 'STOP':
			self.data_changed_flags[10] = 2
			message = {
			'Code' : 'STOP'
			}
			message = json.dumps(message)
			self.data_to_client.put(message)
		elif data == 'UPDATE':
			# Send UPDATE signal
			message = {
			'Code' : 'UPDATE',
			'Time' : extra_data
			}
			message = json.dumps(message)
			self.data_to_client.put(message)
		elif data == 'QUERY RESPONSE':
			#process extra data (dictionary or maybe json)
			self.data_to_client.put('QUERY')
			
		return

	def allow_login_handler(self, state):
		if(state == Qt.Checked):
			# Allow logins
			self.set_flags(2, 1)
		else:
			# Stop logins
			self.set_flags(2, 0)
		return

	def allow_submissions_handler(self, state):
		if(state == Qt.Checked):
			# Allow submissions
			self.set_flags(3, 1)
		else:
			# Stop submissions
			self.set_flags(3, 0)
		return

	def check_login_allowed(self):
		if self.data_changed_flags[2] == 1:
			return True
		return False

	def check_submission_allowed(self):
		if self.data_changed_flags[3] == 1:
			return True
		return False

	def set_flags(self, index, value):
		self.data_changed_flags[index] = value
		return


	#####################################################
	# Databse related functions
	def init_qt_database(self):
		try:
			db = QSqlDatabase.addDatabase('QSQLITE')
			db.setDatabaseName('server_database.db')
			return db
		except:
			print('[ CRITICAL ] Database loading error!')


	def manage_models(self, db, table_name):
		if db.open():
			model = QSqlTableModel()
			model.setTable(table_name)
			model.setEditStrategy(QSqlTableModel.OnFieldChange)
			model.select()
		return model


	def generate_view(self, model):
		table = QTableView()
		table.setModel(model)
		# Enable sorting in the table view
		table.setSortingEnabled(True)
		# Enable Alternate row colors for readablity
		table.setAlternatingRowColors(True)
		# Select whole row when clicked
		table.setSelectionBehavior(QAbstractItemView.SelectRows)
		# Allow only one row to be selected
		table.setSelectionMode(QAbstractItemView.SingleSelection)
		# fit view to whole space
		table.resizeColumnsToContents()
		# Make table non-editable
		table.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# Set view to delete when gui is closed
		table.setAttribute(Qt.WA_DeleteOnClose)

		horizontal_header = table.horizontalHeader()
		horizontal_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header = table.verticalHeader()
		#vertical_header.setSectionResizeMode(QHeaderView.Stretch)
		vertical_header.setVisible(False)
		return table

	@pyqtSlot()
	def create_accounts(self):
		if self.data_changed_flags[4] == 0:
			# CRITICAL section flag set
			self.data_changed_flags[4] = 1
			self.window = new_accounts_ui(self.data_changed_flags)
			self.window.show()			
		else:
			pass
		return

	@pyqtSlot()
	def query_reply(self, selected_row):
		if self.data_changed_flags[8] == 0:
			# CRITICAL section flag set
			self.data_changed_flags[8] = 1
			try:
				query = self.query_model.index(selected_row, 2).data()
				client_id = self.query_model.index(selected_row, 1).data()
				query_id = self.query_model.index(selected_row, 0).data()
			except Exception as error: 
				# Reset data_changed_flag for deletion of account
				print('[ ERROR ] : ' + str(error))
				self.data_changed_flags[8] = 0
				return
			self.window = query_reply_ui(self.data_changed_flags,self.data_to_client ,query,client_id, query_id)
			self.window.show()			
		else:
			pass
		return

	@pyqtSlot()
	def delete_account(self, selected_rows):
		if self.data_changed_flags[6] == 0:
			# Set critical flag
			self.data_changed_flags[6] = 1
		else:
			# If one data deletion window is already opened, process it first.
			return
		# If no row is selected, return
		try:
			username = str(selected_rows[0].data())
		except: 
			# Reset data_changed_flag for deletion of account
			self.data_changed_flags[6] = 0
			return
		message = "Are you sure you want to delete : " + username + " ? "
	
		custom_close_box = QMessageBox()
		custom_close_box.setIcon(QMessageBox.Critical)
		custom_close_box.setWindowTitle('Confirm Deletion')
		custom_close_box.setText(message)

		custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		custom_close_box.setDefaultButton(QMessageBox.No)

		button_yes = custom_close_box.button(QMessageBox.Yes)
		button_yes.setText('Yes')
		button_no = custom_close_box.button(QMessageBox.No)
		button_no.setText('No')

		button_yes.setObjectName("close_button_yes")
		button_no.setObjectName("close_button_no")

		button_yes.setStyleSheet(open('Elements/style.qss', "r").read())
		button_no.setStyleSheet(open('Elements/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			user_management.delete_user(username)
			# Update Accounts View
			self.data_changed_flags[5] = 1
		elif custom_close_box.clickedButton() == button_no : 
			pass

		# Reset critical flag
		self.data_changed_flags[6] = 0

		return

	###################################################
	
	###################################################

	def set_status(self, message = 'STOPPED'):
		self.status.showMessage('BitsOJ > ' + message)
	###################################################

	def closeEvent(self, event):
		message = "Pressing 'Yes' will SHUT the Server.\nAre you sure you want to exit?"
		detail_message = "Any active contest might end prematurely. "
		
		custom_close_box = QMessageBox()
		custom_close_box.setIcon(QMessageBox.Critical)
		custom_close_box.setWindowTitle('Warning!')
		custom_close_box.setText(message)
		custom_close_box.setInformativeText(detail_message)

		custom_close_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		custom_close_box.setDefaultButton(QMessageBox.No)

		button_yes = custom_close_box.button(QMessageBox.Yes)
		button_yes.setText('Yes')
		button_no = custom_close_box.button(QMessageBox.No)
		button_no.setText('No')

		button_yes.setObjectName("close_button_yes")
		button_no.setObjectName("close_button_no")

		button_yes.setStyleSheet(open('Elements/style.qss', "r").read())
		button_no.setStyleSheet(open('Elements/style.qss', "r").read())

		custom_close_box.exec_()

		if custom_close_box.clickedButton() == button_yes:
			event.accept()
		elif custom_close_box.clickedButton() == button_no : 
			event.ignore()


class init_gui(server_window):
	# data_from_interface queue is data_to_client queue with respect to interface
	def __init__(self, data_changed_flags, data_to_client):
		# make a reference of App class
		app = QApplication(sys.argv)
		app.setStyle("Fusion")
		app.setStyleSheet(open('Elements/style.qss', "r").read())
		# If user is about to close window
		app.aboutToQuit.connect(self.closeEvent)
		
		server_app = server_window(data_changed_flags, data_to_client)

		# Splash screen
		# splash = QSplashScreen(QPixmap("Elements/bitwise.png"))
		# splash.show()
		# splash.finish(server_app)	
		# Splash ends

		server_app.showMaximized()

		# Execute the app mainloop
		app.exec_()
		return