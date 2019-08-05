from PyQt5.QtCore import QThread, pyqtSignal


class GetTimeTableThread(QThread):
    """
        A thread for refresh timetable
    """
    sig = pyqtSignal(list)

    def __init__(self, sc):
        QThread.__init__(self)
        self.sc = sc

    def __del__(self):
        self.wait()

    def run(self):
        # Emit signal to trigger the update table function
        tmp = self.sc.get_timetable(self.date)

        self.sig.emit(tmp)

    # Override the start function which takes one more parameter
    def start(self, date):
        self.date = date
        super(GetTimeTableThread, self).start()


class LoginThread(QThread):
    """
        A thread for login
    """
    sig = pyqtSignal(str)

    def __init__(self, sc):
        QThread.__init__(self)
        self.sc = sc

    def __del__(self):
        self.wait()

    def run(self):
        tmp = self.sc.login()
        self.sig.emit(tmp)
