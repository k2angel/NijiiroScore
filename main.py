import glob
import os
import shutil
from logging import (DEBUG, INFO, FileHandler, Formatter, StreamHandler,
                     getLogger)


def make_logger(name):
    logger = getLogger(name)
    logger.setLevel(DEBUG)

    st_handler = StreamHandler()
    st_handler.setLevel(INFO)
    st_handler.setFormatter(Formatter("[{levelname}] {message}", style="{"))
    logger.addHandler(st_handler)

    fl_handler = FileHandler(filename=".log", encoding="utf-8", mode="w")
    fl_handler.setLevel(DEBUG)
    fl_handler.setFormatter(
        Formatter(
            "[{levelname}] {asctime} [{filename}:{lineno}] {message}", style="{"
        )
    )
    logger.addHandler(fl_handler)

    return logger


genres = ["01-J-POP", "02-アニメ", "03-ボーカロイド", "04-ゲームミュージック", "05-バラエティ", "06-クラシック",
          "07-ナムコオリジナル", "08-キッズ"]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logger = make_logger(__name__)
    oldnijiiro = input("今のニジイロ全曲フォルダーのパス\n> ")
    logger.debug(f"OldNijiiro: {oldnijiiro}")
    newnijiiro = input("新しいニジイロ全曲フォルダー､もしくはzipファイルのパス\n> ")
    logger.debug(f"NewNijiiro: {newnijiiro}")
    if os.path.splitext(newnijiiro)[1] == ".zip":
        logger.info("Extract...")
        shutil.unpack_archive(newnijiiro, "./nijiiro")
        newnijiiro = "./nijiiro"
        logger.info("Complete.")
    genres = [genre for genre in genres if os.path.exists(os.path.join(oldnijiiro, genre))]
    logger.debug(genres)
    for genre in genres:
        oldnijiiro_tjas = list()
        newnijiiro_tjas = list()
        [oldnijiiro_tjas.append(tja) for tja in glob.glob(os.path.join(oldnijiiro, genre) + "\**\*.tja", recursive=True)]
        [newnijiiro_tjas.append(tja) for tja in glob.glob(os.path.join(newnijiiro, genre) + "\**\*.tja", recursive=True)]
        for tja in oldnijiiro_tjas:
            filename = os.path.basename(tja)
            newnijiiro_dir = [p for p in newnijiiro_tjas if os.path.basename(p) == filename[filename.find(",") + 1 : len(filename)]]
            if newnijiiro_dir == []:
                continue
            scores = [score for score in glob.glob(f"{tja}*.score.ini")]
            if scores == []:
                continue
            for score in scores:
                newnijiiro_score = os.path.splitext(newnijiiro_dir[0])[0] + os.path.basename(score).replace(os.path.splitext(filename)[0], '')
                shutil.copy(score, newnijiiro_score)
                print(f"{score} -> {newnijiiro_score} copied.")