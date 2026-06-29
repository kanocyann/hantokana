from PySide6.QtNetwork import QLocalServer, QLocalSocket


class SingleInstanceApplication:
    """单例应用程序类，确保只有一个实例在运行"""

    def __init__(self, app_id, activate_callback=None):
        self.app_id = app_id
        self.activate_callback = activate_callback
        self.server = None
        self.is_running = False

    def try_connect_to_instance(self):
        socket = QLocalSocket()
        socket.connectToServer(self.app_id)

        if socket.waitForConnected(500):
            socket.write(b"ACTIVATE")
            socket.flush()
            socket.waitForBytesWritten(1000)
            socket.disconnectFromServer()
            return True

        return False

    def start_server(self):
        self.server = QLocalServer()
        QLocalServer.removeServer(self.app_id)

        if not self.server.listen(self.app_id):
            print(f"无法启动本地服务器: {self.server.errorString()}")
            return False

        self.server.newConnection.connect(self.handle_connection)
        return True

    def handle_connection(self):
        socket = self.server.nextPendingConnection()
        if socket.waitForReadyRead(1000):
            data = socket.readAll().data()
            if data == b"ACTIVATE" and self.activate_callback:
                self.activate_callback()

        socket.disconnectFromServer()

    def ensure_single_instance(self):
        if self.try_connect_to_instance():
            self.is_running = True
            return False

        if self.start_server():
            self.is_running = False
            return True

        self.is_running = True
        return False
