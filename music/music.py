import os
import json
from database_music import MusicDatabase

from tinytag import TinyTag
from progress.bar import Bar

class Music():
    def __init__(self, config):
        self.db = MusicDatabase(config["music_db"], True)

        for folder in config["music_folders"]:
            self.crawl_folder(os.path.join(config["music_root"], folder))
    
    def crawl_folder(self, folder):
        files = 0
        folders = 0
        for dir_path, dir_names, file_names in os.walk(folder):
            files += len(file_names)
            folders += len(dir_names)

        print("Amount of files to process: " + str(files))
        print("Amount of folders to process: " + str(folders))

        bar = Bar('Processing books on disk: ', max=folders)

        for dir_path, dir_names, file_names in os.walk(folder):
            albums = []
            for file in file_names:
                try:
                    tag = TinyTag.get(os.path.join(dir_path, file))
                    music_file = {}
                    music_file["album"] = tag.album         # album as string
                    music_file["albumartist"] = tag.albumartist   # album artist as string
                    music_file["artist"] = tag.artist        # artist name as string
                    music_file["audio_offset"] = tag.audio_offset  # number of bytes before audio data begins
                    music_file["bitrate"] = tag.bitrate       # bitrate in kBits/s
                    music_file["comment"] = tag.comment       # file comment as string
                    music_file["composer"] = tag.composer      # composer as string 
                    music_file["disc"] = tag.disc          # disc number
                    music_file["disc_total"] = tag.disc_total    # the total number of discs
                    music_file["duration"] = tag.duration      # duration of the song in seconds
                    music_file["filesize"] = tag.filesize      # file size in bytes
                    music_file["genre"] = tag.genre         # genre as string
                    music_file["samplerate"] = tag.samplerate    # samples per second
                    music_file["title"] = tag.title         # title of the song
                    music_file["track"] = tag.track         # track number as string
                    music_file["track_total"] = tag.track_total   # total number of tracks as string
                    music_file["year"] = tag.year          # year or data as string
                    music_file = (None, tag.album, tag.albumartist, tag.artist, tag.audio_offset, tag.bitrate, tag.comment, tag.composer, tag.disc, tag.disc_total, tag.duration, tag.filesize, tag.genre, tag.samplerate, tag.title, tag.track, tag.track_total, tag.year, str(os.path.join(dir_path, file)))
                    albums.append(music_file)
                except Exception as e:
                    print(e)
                    #logger.error(e)
                self.db.insert_data_table("music", self.db.music_columns, albums)
            bar.next()
        bar.finish()

if __name__ == "__main__":
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.json")) as json_file:
            config = json.load(json_file)
    except:
        print("config.json is not found!")
        exit()
    
    music = Music(config)