class ExtractColour:

    TELEGRAM_GET_FILE_API = "https://api.telegram.org/bot{}/getFile?file_id={}"
    TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot{}/{}"
    IMAGGA_API = "https://api.imagga.com/v1/colors?url={}"
    FGCOLOUR, BGCOLOUR = ("FGCOLOUR", "BGCOLOUR")  # caption to choose extract method

    def __init__(self, photo_id):
        self.photo_id = photo_id

    @property
    def state(self):
        return (ExtractColour.FGCOLOUR if self.__extract_method == self.__extract_fgcolour
                else ExtractColour.BGCOLOUR)

    @state.setter
    def state(self, state):
        if state == ExtractColour.FGCOLOUR:
            self.__extract_method = self.__extract_fgcolour
        else:
            self.__extract_method = self.__extract_bgcolour

    def extract(self):
        pass

    def get_photo_url(self):
        pass

    def __extract_method(self):
        self.state = ExtractColour.BGCOLOUR
        return self.__extract_method()

    def __extract_fgcolour(self):
        pass

    def __extract_bgcolour(self):
        pass
