import os
import warnings

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
        self.__read_file()

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
                if information_category == "Events" or information_category == "TimingPoints" or information_category == "HitObjects":
                    file_information[information_category] = []
                continue

            if information_category == "Events" or information_category == "TimingPoints" or information_category == "HitObjects":
                file_information[information_category].append(line)
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

        general = file_information["General"]
        self.__general = self.__FileTags.General(general['AudioFilename'], general['AudioLeadIn'], general['PreviewTime'],
                                      general['Countdown'], general['SampleSet'], general['StackLeniency'],
                                      general['Mode'], general['LetterboxInBreaks'], general['WidescreenStoryboard'])
        editor = file_information["Editor"]
        self.__editor = self.__FileTags.Editor(editor['DistanceSpacing'], editor['BeatDivisor'], editor['GridSize'], editor['TimelineZoom'])
        metadata = file_information["Metadata"]
        self.__metadata = self.__FileTags.Metadata(metadata['Title'], metadata['TitleUnicode'], metadata['Artist'],
                                                   metadata['ArtistUnicode'], metadata['Creator'], metadata['Version'],
                                                   metadata['Source'], metadata['Tags'], metadata['BeatmapID'], metadata['BeatmapSetID'])
        difficulty = file_information["Difficulty"]
        self.__difficulty = self.__FileTags.Difficulty(difficulty['HPDrainRate'], difficulty['CircleSize'], difficulty['OverallDifficulty'],
                                                       difficulty['ApproachRate'], difficulty['SliderMultiplier'], difficulty['SliderTickRate'])
        self.__events = file_information["Events"]
        self.__timing_points = file_information["TimingPoints"]
        self.__colours = file_information["Colours"]


    @property
    def path(self):
        return self.__path
    @property
    def version(self):
        return self.__version
    @property
    def name(self):
        return self.__name
    @property
    def general(self):
        return self.__general
    @property
    def editor(self):
        return self.__editor
    @property
    def metadata(self):
        return self.__metadata
    @property
    def difficulty(self):
        return self.__difficulty
    @property
    def events(self):
        return self.__events
    @property
    def timing_points(self):
        return self.__timing_points
    @property
    def colours(self):
        return self.__colours

    class HitObjectList:
        class HitObject:
            def __init__(self, x:int, y:int, time:int):
                pass

    class __FileTags:
        class General:
            def __init__(self, audio_file_name:str, audio_lead_in:int,
                         preview_time:int, count_down:int, sample_set:str,
                         stack_leniency:float, mode:int, letter_box_in_breaks:int, widescreen_storyboard:int):
                self.__audio_file_name:str = audio_file_name
                self.__audio_lead_in:int = audio_lead_in
                self.__preview_time:int = preview_time
                self.__count_down:int = count_down
                self.__sample_set:str = sample_set
                self.__stack_leniency:float = stack_leniency
                self.__mode:int = mode
                self.__letter_box_in_breaks:int = letter_box_in_breaks
                self.__widescreen_storyboard:int = widescreen_storyboard

            @property
            def audio_file_name(self) -> str:
                return self.__audio_file_name
            @property
            def audio_lead_in(self) -> int:
                return self.__audio_lead_in
            @property
            def preview_time(self) -> int:
                return self.__preview_time
            @property
            def count_down(self) -> int:
                return self.__count_down
            @property
            def sample_set(self) -> str:
                return self.__sample_set
            @property
            def stack_leniency(self) -> float:
                return self.__stack_leniency
            @property
            def mode(self) -> int:
                return self.__mode
            @property
            def letter_box_in_breaks(self) -> int:
                return self.__letter_box_in_breaks
            @property
            def widescreen_storyboard(self) -> int:
                return self.__widescreen_storyboard
        class Editor:
            def __init__(self, distance_spacing:int, beat_divisor:int, grid_size:int, timeline_zoom:float):
                self.__distance_spacing:int = distance_spacing
                self.__beat_divisor:int = beat_divisor
                self.__grid_size:int = grid_size
                self.__timeline_zoom:float = timeline_zoom

            @property
            def distance_spacing(self):
                return self.__distance_spacing
            @property
            def beat_divisor(self):
                return self.__beat_divisor
            @property
            def grid_size(self):
                return self.__grid_size
            @property
            def timeline_zoom(self):
                return self.__timeline_zoom
        class Metadata:
            def __init__(self, title:str, title_unicode:str, artist:str, artist_unicode:str, creator:str, version:str, source:str, tags:str, beatmap_id:int, beatmap_set_id:int):
                self.__title:str = title
                self.__title_unicode:str = title_unicode
                self.__artist:str = artist
                self.__artist_unicode:str = artist_unicode
                self.__creator:str = creator
                self.__version:str = version
                self.__source:str = source
                self.__tags:str = tags
                self.__beatmap_id:int = beatmap_id
                self.__beatmap_set_id:int = beatmap_set_id

            @property
            def title(self):
                return self.__title
            @property
            def title_unicode(self):
                return self.__title_unicode
            @property
            def artist(self):
                return self.__artist
            @property
            def artist_unicode(self):
                return self.__artist_unicode
            @property
            def creator(self):
                return self.__creator
            @property
            def version(self):
                return self.__version
            @property
            def source(self):
                return self.__source
            @property
            def tags(self):
                return self.__tags
            @property
            def beatmap_id(self):
                return self.__beatmap_id
            @property
            def beatmap_set_id(self):
                return self.__beatmap_set_id
        class Difficulty:
            def __init__(self, hp_drain_rate:float, circle_size:float, overall_difficulty:float, approach_rate:float, slider_multiplier:float, slider_tick_rate:float):
                self.__hp_drain_rate:float = hp_drain_rate
                self.__circle_size:float = circle_size
                self.__overall_difficulty:float = overall_difficulty
                self.__approach_rate:float = approach_rate
                self.__slider_multiplier:float = slider_multiplier
                self.__slider_tick_rate:float = slider_tick_rate

            @property
            def hp_drain_rate(self):
                return self.__hp_drain_rate
            @property
            def circle_size(self):
                return self.__circle_size
            @property
            def overall_difficulty(self):
                return self.__overall_difficulty
            @property
            def approach_rate(self):
                return self.__approach_rate
            @property
            def slider_multiplier(self):
                return self.__slider_multiplier
            @property
            def slider_tick_rate(self):
                return self.__slider_tick_rate
path = "C:\\Users\\arno\\AppData\\Local\\osu!\\Songs\\1024028 ShinRa-Bansho - Marisa wa Taihen na Mono o Nusunde Ikimashita ShinRa-Bansho Ver"

a = Song(path)
print(a.maps[0].timing_points)