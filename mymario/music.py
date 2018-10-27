"""
Module for playing different musics through the game
"""
import os
from threading import main_thread, Thread

from config import MUSIC_FILES_PATH


class Music:
    """
    Class used for playing music during the game
    """
    def __init__(self):
        """
        Initialises the music files with their respective action.
        """
        self.action_music_filename = {
            "Player at start": "start",
            "Player at lake": "lake",
            "Player at thrones": "last",
            "Player at end": "ending",
            "Player jumped": "jump",
            "Game paused": "pause",
            "Game over": "gameover",
            "Player got coin": "coin",
            "Game completed": "finished",
            "Player jumped on enemy": "jumponenemy",
            "Player got power up": "powerup",
            "Player got LIFE": "gotlife",
            "Player got time": "gottime",
            "Player lost LIFE": "lostlife",
            "Player launched stones": "stones",
            "Stone hit enemy": "stoneonenemy"
        }
        self.player_crossed_start = False
        self.player_crossed_lake = False
        self.player_crossed_thrones = False

    @staticmethod
    def _play(filename):
        """
        Plays the given music filename
        :param filename:
        :return:
        """
        if main_thread().is_alive():
            os.system('aplay -q ' + MUSIC_FILES_PATH + filename + '.wav > /dev/null')

    def play_music_for_action(self, action='Player at start ', no_thread=False, change=False):
        """
        Plays the given music
        :param action: Music file name to play
        :param no_thread: boolean whether to play music in parallel or not
        :param change: boolean whether to change the correct music or not
        :return:
        """
        filename = self.action_music_filename[action]
        if change:
            os.system('killall -q aplay 2> /dev/null')
        if not no_thread:
            temp = Thread(target=self._play, args=(filename,))
            temp.daemon = True
            temp.start()
        else:
            self._play(filename)

    def get_filename_from_action(self, action):
        """
        Get the music filename for the corresponding action
        :param action: The action to which the music filename is retrieved
        :return: Music filename for given action
        """
        return self.action_music_filename[action]
