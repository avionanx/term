from enum import Enum

class AbstractMessage:
    def __init__(self, message:str):
        self.message = message
        self.message_type:MessageType = None

class SystemMessage(AbstractMessage):
    def __init__(self, message:str):
        super().__init__(message)
        self.message_type = MessageType.SYSTEM
    def __str__(self) -> str:
        return f"[SYSTEM]: {self.message}"

class UserMessage(AbstractMessage):
    def __init__(self, message:str, user:str):
        super().__init__(message)
        self.message_type = MessageType.USER
        self.user = user
    def __str__(self) -> str:
        return f"{self.user}: {self.message}"

class MessageType(Enum):
    SYSTEM = 1
    USER = 2