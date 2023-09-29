import glob
import os
import shutil

genres = ["01-J-POP", "02-アニメ", "03-ボーカロイド", "04-ゲームミュージック", "05-バラエティ", "06-クラシック",
          "07-ナムコオリジナル", "08-キッズ"]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    oldnijiiro = input("今のニジイロ全曲フォルダーのパス\n> ")
    print(f"OldNijiiro: {oldnijiiro}")
    newnijiiro = input("新しいニジイロ全曲フォルダー､もしくはzipファイルのパス\n> ")
    print(f"NewNijiiro: {newnijiiro}")
    if os.path.splitext(newnijiiro)[1] == ".zip":
        print("Extract...")
        shutil.unpack_archive(newnijiiro, "./nijiiro")
        newnijiiro = "./nijiiro"
        print("Complete.")
    genres = [genre for genre in genres if os.path.exists(os.path.join(oldnijiiro, genre))]
    for genre in genres:
        print(genre)
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
        shutil.rmtree(os.path.join(oldnijiiro, genre))
        print(f"{os.path.join(oldnijiiro, genre)} deleted.")

    for dir in glob.glob(newnijiiro+"\*/"):
        path = shutil.move(dir, oldnijiiro)
        print(f"{dir} -> {path} moved.")