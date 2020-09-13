class EnteredRecord:
    def __init__(self) -> None:
        self.entered = False
    
    def __enter__(self) -> None:
        self.entered = True
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.entered = False

def print_track_async(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except:
            import traceback
            traceback.print_exc()
    return wrapper