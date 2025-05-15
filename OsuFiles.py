import os


class Song:
    def __init__(self, song_path:str):
        self.__song_path = song_path

        self.__maps:list[Map] = []
        self.__sounds_paths:list[str] = []
        self.__backgrounds_paths:list[str] = []

        self.__file_repartition()



    def __file_repartition(self):
        for file in os.listdir(self.__song_path):
            file_extension = file.split(".")[-1]

            if file_extension == "osu":
                self.maps.append(Map(f"{self.__song_path}\\{file}"))
                continue
            if file_extension == "wav" or file_extension == "mp3":
                self.__sounds_paths.append(f"{self.__song_path}\\{file}")
                continue
            if file_extension == "png" or file_extension == "jpg":
                self.__backgrounds_paths.append(f"{self.__song_path}\\{file}")
                continue

    @property
    def maps(self):
        return self.__maps
    @property
    def sounds_paths(self):
        return self.__sounds_paths
    @property
    def backgrounds_paths(self):
        return self.backgrounds_paths

class Map:
    def __init__(self, map_path):
        self.__path = map_path
        self.__name = map_path.split("\\")[-1]
        self.file_information = self.__read_file()

    def __read_file(self):
        file = open(self.path, "r", encoding="utf-8")
        file_information = {}
        information_category = ""
        for index, line in  enumerate(file):
            line = line.strip()

            if index == 0:
                self.__version = line
                continue

            if line == "":
                continue

            if line[0] == "[" and line[-1] == "]":
                information_category = line[1:-1]
                file_information[information_category] = {}
                continue

            if information_category != "":
                information = line.split(":")[0]
                data = line.split(":")[-1].strip()
                if data.isdigit():
                        data = int(data)
                elif "." in data:
                    only_digit = True
                    for i in data.split("."):
                        if not i.isdigit():
                            only_digit = False
                    if only_digit:
                        data = float(data)
                file_information[information_category][information] = data

        return file_information

    @property
    def path(self):
        return self.__path
    @property
    def version(self):
        return self.__version
    @property
    def name(self):
        return self.__name

    class General:
        def __init__(self, audio_file_name:str, audio_lead_in:int,
                     preview_time:int, count_down:int, sample_set:str,
                     stack_leniency:float, mode:int, letter_box_in_breaks:int, widescreen_storyboard:int):
            self.audio_file_name:str = audio_file_name
            self.audio_lead_in:int = audio_lead_in
            self.preview_time:int = preview_time
            self.count_down:int = count_down
            self.sample_set:str = sample_set
            self.stack_leniency:float = stack_leniency
            self.mode:int = mode
            self.letter_box_in_breaks:int = letter_box_in_breaks
            self.widescreen_storyboard:int = widescreen_storyboard



path = "C:\\Users\\arnos\\AppData\\Local\\osu!\\Songs\\682290 Hige Driver - Miracle Sugite Yabai (feat shully)"

a = Song(path)
print(a.maps[0].file_information)