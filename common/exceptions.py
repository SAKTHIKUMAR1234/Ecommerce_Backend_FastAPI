

class CustomeException(Exception):
  
  def __init__(self, *args: object) -> None:
    super().__init__(*args)
    
class InvalidDataException(Exception):
  
  def __init__(self, *args: object) -> None:
    super().__init__(*args)