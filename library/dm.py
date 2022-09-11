import sys
import os


class download_manager():
    def __init__(self, link: str, directory: str = None, filename: str = None, category_index: int = None):
        self.link = link
        if directory == None:
            self.folder = ''
        else:
            self.folder = f' --folder="{directory}" '
        if filename == None:
            self.filename = ''
        else:
            self.filename = f' --filename="EP{filename.zfill(2)}.mp4" '
        if category_index == None:
            self.category = -1
        else:
            self.category = category_index
        if sys.platform == 'linux':
            self.uGet(self)

    def uGet(self):
        """uGet Download Manager For Linux Only"""
        command = f'nohup uget-gtk --category-index={self.category} --quiet{self.folder}{self.filename}"{self.link}" > /dev/null 2>&1 &'
        os.system(command)

    def IDM(self):
        pass

    def aria2c(self):
        """
        In development coming soon...
        """
        # source: https://pypi.org/project/aria2p/
        pass
