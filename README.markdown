Informant - An Information Board
================================

Panes
-----
	Assignments
	Todo
	Clock
	Classes
	Time until wake
	Unread Email?

Management
----------
	Data synced from server on internet - accessable anywhere
	Events can be sent from email?

Hardware requirements
---------------------
	A large screen
	Hardware capable of running an operating system

Technologies
------------
	Output needs to be beautiful and responsive
	Possiblities:
		Webpage:
			Powered by PHP, output using elements or HTML5 canvas
			Google Chrome has beautiful font rendering
			Ajax for data sync, handled by Javascript
			Might be hard to handle stuff that needs to be persistant, like an IMAP connection
			Very big pro: easy to set up anywhere, assuming it's on an internet site (maybe shouldn't be for any practical use)
		Executable:
			Perhaps powered by Java
			Obviously data syncronization would be instant
			Output may look awful

Internal Handling
-----------------
	Each section has its own 'pane', which consists of server- and client-side logic code, media files, and rendering code.