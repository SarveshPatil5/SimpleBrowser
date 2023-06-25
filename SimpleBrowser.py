# importing libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import webbrowser, json, os, sys, datetime
from json.decoder import JSONDecodeError

# creating main window class
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		# ADD TAB WIGDETS TO DISPLAY WEB TABS
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.setTabsClosable(True)
		self.setCentralWidget(self.tabs)
		self.setGeometry(100, 100, 1000, 700)
		self.history = []

        # ADD DOUBLE CLICK EVENT LISTENER
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        # ADD TAB CLOSE EVENT LISTENER
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # ADD ACTIVE TAB CHANGE EVENT LISTENER
		self.tabs.currentChanged.connect(self.current_tab_changed)

		self.status = QStatusBar()
		self.setStatusBar(self.status)

        # ADD NAVIGATION TOOLBAR
		navtb = QToolBar("Navigation")
		navtb.setIconSize(QSize(20, 20))
		self.addToolBar(navtb)
		
        #### ADD BUTTONS TO NAVIGATION TOOLBAR
        # PREVIOUS WEB PAGE BUTTON
		back_btn = QAction(QIcon(os.path.join('icons', 'left.svg')), "Back", self)
		back_btn.setStatusTip("Back to previous page")
		navtb.addAction(back_btn)
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        # NEXT WEB PAGE BUTTON
		next_btn = QAction(QIcon(os.path.join('icons', 'right.svg')), "Forward", self)
		next_btn.setStatusTip("Forward to next page")
		navtb.addAction(next_btn)
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        # REFRESH WEB PAGE BUTTON
		reload_btn = QAction(QIcon(os.path.join('icons', 'reload.svg')), "Reload", self)
		reload_btn.setStatusTip("Reload page")
		navtb.addAction(reload_btn)
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())

		# HOME PAGE BUTTON
		home_btn = QAction(QIcon(os.path.join('icons', 'home.svg')), "Home", self)
		home_btn.setStatusTip("Go home")
		navtb.addAction(home_btn)
		home_btn.triggered.connect(self.navigate_home)

		# Separator in the tool bar
		navtb.addSeparator()
		
		# Google Page BUTTON
		google_btn = QAction(QIcon(os.path.join('icons', 'google-logo.png')), "Google", self)
		google_btn.setStatusTip("Google")
		navtb.addAction(google_btn)
		google_btn.triggered.connect(self.navigate_google)
		
        # ADD LINE EDIT TO SHOW AND EDIT URLS
		self.urlbar = QLineEdit()
		navtb.addWidget(self.urlbar)
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# Separator in the tool bar
		navtb.addSeparator()
		
        # ADD STOP BUTTON TO STOP URL LOADING
		stop_btn = QAction(QIcon(os.path.join('icons', 'stop.svg')), "Stop", self)
		stop_btn.setStatusTip("Stop loading current page")
		navtb.addAction(stop_btn)
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

		# creating a button for bookmark
		bookmark_btn = QAction(QIcon(os.path.join('icons', 'bookmark.svg')), "Add Bookmark", self)
		bookmark_btn.setStatusTip("Bookmark this page")
		navtb.addAction(bookmark_btn)
		bookmark_btn.triggered.connect(self.add_bookmark)

		# ADD FILE MENU ACTIONS
		file_menu = self.menuBar().addMenu("&Tab+")

        # ADD FILE MENU ACTIONS
		new_tab_action = QAction(QIcon(os.path.join('icons', 'cil-library-add.png')), "New Tab", self)
		new_tab_action.setStatusTip("Open a new tab")
		file_menu.addAction(new_tab_action)
		# ADD NEW TAB
		new_tab_action.triggered.connect(lambda _: self.add_new_tab())
		self.add_new_tab(QUrl.fromLocalFile("/Home.html"))

		# creating a menu for bookmarks
		# adding this menu to the menu bar
		bookmark_menu = self.menuBar().addMenu("&Bookmarks")
		show_bookmarks = QAction("Show Bookmarks", self)
		bookmark_menu.addAction(show_bookmarks)
		show_bookmarks.triggered.connect(self.show_bookmark)

		# Help menu
		help_menu = self.menuBar().addMenu("&Help")
		# ADD HELP MENU ACTIONS
		navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')), "Homepage", self)
		navigate_home_action.setStatusTip("Go to Homepage")
		help_menu.addAction(navigate_home_action)
		# NAVIGATE TO DEVELOPER WEBSITE
		navigate_home_action.triggered.connect(self.navigate_home)

		# creating a button for History
		history_btn = QAction(QIcon(os.path.join('icons', 'history.svg')), "Show History", self)
		history_btn.setStatusTip("Show History")
		
		navtb.addAction(history_btn)
		history_btn.triggered.connect(self.show_history)

		# STYLESHEET TO CUSTOMIZE WINDOW
		self.setStyleSheet("""
		
		/*Body */
		QWidget{
           background-color:#202832;
           color: rgb(255, 255, 255);
        }
		/* The tab widget frame */
		QTabWidget::pane { 
            border-top: 2px solid rgb(90, 90, 90);
            position: absolute;
            color: rgb(255, 255, 255);
        }
		/* New Tab Css */
		QTabBar::tab {
			width: 100%;
			background-color:#202832;
			margin: 0.1em;
			padding: 0.3em;
			font-size:14px;
			border : 1px solid white; 
			border-radius : 4px;
		}
		QTabBar::tab:hover{
			background: rgb(49, 49, 49);
            border: 1px solid aqua;
            background-color:#0d1117;
	    	border-radius: 4px;
		}
		QTabBar::tab:selected{
			background: rgb(49, 49, 49);
            border: 1px solid #112740;
            background-color:#0d1117;
		    border-radius: 4px;
			border:1px solid yellow;
		}
		/*searchbar*/
		QLineEdit {
            border: 2px solid #112740;
            border-radius: 10px;
            padding: 5px;
	    	margin-right:50px;
            background-color:#0d1117;
            color: rgb(255, 255, 255);
        }
        QLineEdit:hover {
            border: 2px solid white;
        }
        QLineEdit:focus{
            border: 2px solid rgb(0, 136, 255);
            color: rgb(200, 200, 200);
        }
        QPushButton{
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }
		/*Button*/
		QLabel:hover{
            
            border: 2px solid #112740;
            
	    	border-radius: 10px;
        }
		QToolButton::hover{
            background: rgb(49, 49, 49);
            border: 2px solid #112740;
            background-color:#0d1117;
	    	border-radius: 10px;
        }
		
		""")

		# SHOW MAIN WINDOW
		self.show()

	#*********** FUNCTION ***********#

	    # ADD NEW WEB TAB
	def add_new_tab(self, qurl=None, label="Loading..."):
        # Check if url value is blank
		if qurl is None:
			qurl = QUrl.fromLocalFile("/Home.html")
        
		# Load the passed url
		browser = QWebEngineView()
		browser.setUrl(qurl)

        # ADD THE WEB PAGE TAB
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

        # ADD BROWSER EVENT LISTENERS
        # On URL change
		browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        # On loadfinished
		browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
									 
		browser.loadFinished.connect(lambda qurl, browser=browser:
                               self.add_history(qurl, browser)) # Connect to add_history method
		
    # ADD NEW TAB ON DOUBLE CLICK ON TABS
	def tab_open_doubleclick(self, i):
		if i == -1:  # No tab under the click
			self.add_new_tab()

    # CLOSE TABS 
	def close_current_tab(self, i):
		if self.tabs.count() < 2: #Only close if there is more than one tab open
			return

		self.tabs.removeTab(i)

	# method for updating url
	# this method is called by the QWebEngineView object
	def update_urlbar(self, q, browser):

		if browser != self.tabs.currentWidget():
			
			return
		
        # URL Schema
		if q.scheme() == 'https':
			pass
			
			
		else:
			pass
			
			# setting text to the url bar
			
			# setting cursor position of the url bar

		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

	def current_tab_changed(self, i):
        # i = tab index
        # GET CURRENT TAB URL
		qurl = self.tabs.currentWidget().url()
        # UPDATE URL TEXT
		self.update_urlbar(qurl, self.tabs.currentWidget())
        # UPDATE WINDOWS TITTLE
		self.update_title(self.tabs.currentWidget())

	# method for updating the title of the window
	def update_title(self, browser):
		if browser != self.tabs.currentWidget():
		# If this signal is not from the current ACTIVE tab, ignore
			return

		title = self.tabs.currentWidget().page().title()
		self.setWindowTitle("% s - Simple Browser" % title)

	# home action
	def navigate_home(self, browser):
		self.tabs.currentWidget().setUrl(QUrl.fromLocalFile("/Home.html"))
		
	# Google action 
	def navigate_google(self, browser):
		self.tabs.currentWidget().setUrl(QUrl("http://google.com"))

	# method called by the line edit when return key is pressed
	def navigate_to_url(self):

		# getting url and converting it to QUrl object
		q = QUrl(self.urlbar.text())

		# if url is scheme is blank
		if q.scheme() == "":
			# set url scheme to html
			q.setScheme("http")

		# set the url to the browser
		self.tabs.currentWidget().setUrl(q)

	# method for adding bookmark
	def add_bookmark(self):
    # get the current page's title and url
		title = self.tabs.currentWidget().title()
		url = self.tabs.currentWidget().url().toString()
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
    # create a bookmark object with title and url
		bookmark = {"title": title, "url": url, "date": date}

    # load the existing bookmarks from file
		with open("bookmarks.json", "r") as f:
			try:
				bookmarks = json.load(f)
			except JSONDecodeError:
				bookmarks = []

    # add the new bookmark to the list of bookmarks
		bookmarks.append(bookmark)

    # save the updated bookmarks to file
		with open("bookmarks.json", "w") as f:
			json.dump(bookmarks, f, indent=1)

    # show a message box to inform the user
		msg_box = QMessageBox()
		msg_box.setText(f"Bookmark added for {title}")
		msg_box.exec_()
		self.show_bookmark()

	def show_bookmark(self):
    # load the existing bookmarks from file
	
		with open("bookmarks.json", "r") as f:
			try:
				bookmarks = json.load(f)
			except JSONDecodeError:
				bookmarks = []

    	# create a dialog to display the bookmarks
		dialog = QDialog(self)
		dialog.setWindowTitle("Bookmarks")
		dialog.setMinimumWidth(500)
		dialog.setMinimumHeight(300)

   		# create a list widget to display the bookmarks
		list_widget = QListWidget(dialog)
		list_widget.itemDoubleClicked.connect(self.navigate_to_bookmark)
		dialog_layout = QVBoxLayout(dialog)
		dialog_layout.addWidget(list_widget)

    	# add the bookmarks to the list widget
		for bookmark in bookmarks:
			item = QListWidgetItem(bookmark["title"])
			item.setData(Qt.UserRole, bookmark["url"])
			list_widget.addItem(item)

    	# show the dialog
		dialog.exec_()

	# method for navigating to a bookmark
	def navigate_to_bookmark(self, item):
		url = item.data(Qt.UserRole)
		self.tabs.currentWidget().load(QUrl(url))

	def add_history(self, qurl, browser):
    # get the current page's title and url
		title = self.tabs.currentWidget().title()
		url = self.tabs.currentWidget().url().toString()
		date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
    # create a history object with title and url
		record = {"title": title, "url": url, "date": date}

    # load the existing history from file
		with open("history.json", "r") as f:
			try:
				history = json.load(f)
			except JSONDecodeError:
				history = []

    # add the new record to the list of history
		history.append(record)

    # save the updated history to file
		with open("history.json", "w") as f:
			json.dump(history, f, indent=1)

	def show_history(self):
    # load the existing history from file
		with open("history.json", "r") as f:
			try:
				history = json.load(f)
			except JSONDecodeError:
				history = []

    	# create a dialog to display the history
		dialog = QDialog(self)
		dialog.setWindowTitle("Web History")
		dialog.setMinimumWidth(800)
		dialog.setMinimumHeight(500)

   		# create a list widget to display the history
		list_widget = QListWidget(dialog)
		list_widget.itemDoubleClicked.connect(self.navigate_to_history)
		dialog_layout = QVBoxLayout(dialog)
		dialog_layout.addWidget(list_widget)

    	# add the history to the list widget
		for record in history:
			item = QListWidgetItem(record["title"])
			item.setData(Qt.UserRole, record["url"])
			list_widget.addItem(item)

    	# show the dialog
		dialog.exec_()

	# method for navigating to a history
	def navigate_to_history(self, item):
		url = item.data(Qt.UserRole)
		self.tabs.currentWidget().load(QUrl(url))

# creating a pyQt5 application
app = QApplication(sys.argv)

# name to the application
app.setApplicationName("Simple Browser")

# creating a main window object
window = MainWindow()

# loop
app.exec_()
