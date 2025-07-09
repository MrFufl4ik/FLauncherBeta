from src.logs.ColorHelper import ColorHelper, ColorCode


class LogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def send_info_log(self, info_text: str):
        print(f"[Info] {info_text}")

    def send_warn_log(self, warn_text: str):
        print(f"{ColorHelper.colorize("[Warning]", [ColorCode.FG_YELLOW.value])} {warn_text}")

    def send_error_log(self, error_text: str):
        print(f"{ColorHelper.colorize("[Error]", [ColorCode.FG_RED.value])} {error_text}")

    def send_success_log(self, success_text: str):
        print(f"{ColorHelper.colorize("[Success]", [ColorCode.FG_GREEN.value])} {success_text}")