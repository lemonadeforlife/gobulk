import sys
import os


class download_manager():
    def __init__(self, link: str, directory: str = None, filename: str = None, category_index: int = None):
        self.link = link
        if directory == None:
            self.folder = ''
        else:
            self.folder = directory
        if filename == None:
            self.filename = ''
        else:
            self.filename = f"EP{str(filename).zfill(2)}.mp4"
        if category_index == None:
            self.category = -1
        else:
            self.category = category_index

    @property
    def uGet(self):
        if self.folder != None:
            self.folder_uget = f' --folder="{self.folder}" '
        if self.filename != None:
            self.filename_uget = f' --filename="EP{str(self.filename).zfill(2)}.mp4" '
        """uGet Download Manager For Linux Only"""
        command = f'nohup uget-gtk --category-index={self.category} --quiet{self.folder.uget}{self.filename_uget}"{self.link}" > /dev/null 2>&1 &'
        os.system(command)

    @property
    def aria2c(self):
        """
        aria2c baby heheboi...
        """
        command = f"""aria2c --dir="{self.folder}" --out="{self.filename}"  --file-allocation='none' -c --max-concurrent-downloads=4 --max-connection-per-server=16 --enable-http-keep-alive=true --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" {self.link}"""
        os.system(command)
