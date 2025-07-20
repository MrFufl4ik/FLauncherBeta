class WindowManager:
    _instance = None

    def __init__(self):
        if hasattr(self, '_initialized'): return
        self._initialized = True
        self.main_window = None
        self.server_loading_window = None
        self.download_window = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_main_window(self) -> 'FLauncherBetaMainWindow':
        if self.has_main_window(): return self.get_main_window()
        from src.windows.main_window.FLauncherBetaMainWindow import FLauncherBetaMainWindow
        self.main_window = FLauncherBetaMainWindow()
        return self.get_main_window()
    def has_main_window(self) -> bool:
        return self.get_main_window() is not None
    def get_main_window(self) -> 'FLauncherBetaMainWindow':
        return self.main_window

    def create_server_loading_window(self) -> 'FLauncherBetaServerLoadingWindow':
        if self.has_server_loading_window(): return self.get_server_loading_window()
        from src.windows.loading_window.FLauncherBetaServerLoadingWindow import FLauncherBetaServerLoadingWindow
        self.server_loading_window = FLauncherBetaServerLoadingWindow()
        return self.get_server_loading_window()
    def has_server_loading_window(self) -> bool:
        return self.get_server_loading_window() is not None
    def distruct_server_loading_window(self):
        self.server_loading_window = None
    def get_server_loading_window(self) -> 'FLauncherBetaServerLoadingWindow':
        return self.server_loading_window

    def create_download_window(self) -> 'FLauncherBetaDownloadWindow':
        if self.has_download_window(): return self.get_download_window()
        from src.windows.download_window.FLauncherBetaDownloadWindow import FLauncherBetaDownloadWindow
        self.download_window = FLauncherBetaDownloadWindow()
        return self.get_download_window()
    def distruct_download_window(self):
        self.download_window = None
    def has_download_window(self) -> bool:
        return self.get_download_window() is not None
    def get_download_window(self) -> 'FLauncherBetaDownloadWindow':
        return self.download_window