import os
import datetime
import shutil
import sys

class Backup:
    total_modified = 0
    def __init__(self, disk: str = "D") -> None:
        for e in [disk, "D", "E", "F"]:
            if self.__is_connected(e):
                self.path = f"{e}:\\backup\\automatic_backup\\"
                break
        else:
            self.path = "F:\\backup\\automatic_backup\\"

    def backup(self) -> int:
        if not self.__is_connected():
            print("External storage is not connected!")
            return 1

        if not self.__test_files_exists():
            print("External storage is not setuped!")
            return 2

        with open(self.path + ".timestamp", "rt") as f:
            time = f.read(50)
            time = time.strip()
            last_modified = datetime.datetime.fromtimestamp(float(time))

        with open(self.path + ".backup", "rt") as f:
            for path in f:
                path = path.strip()
                self.__iter_folder(path, last_modified.timestamp())

        with open(self.path + ".timestamp", "wt") as f:
            f.write(str(datetime.datetime.now().timestamp()))

        print("\nLast modified time: " + last_modified.strftime("%H:%M %d.%m.%Y"))
        print(f"Total modified {self.total_modified} files.\n")

        return 0


    def setup(self) -> int:
        if not self.__is_connected():
            print("External storage is not connected!")
            return 1

        if not os.path.isdir(self.path + "automatic_backup"):
            os.makedirs("D:\\backup\\automatic_backup")

        with open(self.path + ".backup", "at") as f:
            f.write("")

        with open(self.path + ".timestamp", "wt") as f:
            f.write(str(1))

        print("Backup setuping succeed.")
        return self.backup()
        
        
    def add(self) -> None:
        from tkinter.filedialog import askdirectory as _askdirectory

        if not self.__is_connected():
            print("External storage is not connected!")
            return None

        if not self.__test_files_exists():
            print("External storage is not setuped!")
            return None

        path = _askdirectory(
            initialdir="C:\\Users\\Fíla\\Desktop", title="Choose directory"
        )
        if path == "":
            print("No path chosen")
            return None

        with open(self.path + ".backup", "at") as f:
            f.write(path)

        print("Adding backuping folder succeed.")
        self.__iter_folder(path, 1)
        self.backup()


    def __iter_folder(self, path: str, last_modified: float) -> None:
        for file_name in os.listdir(path):
            if file_name[0] == "." or file_name[:4] == "venv":
                continue
            if not os.path.isdir(path + "\\" + file_name):
                time = os.path.getmtime(path + "\\" + file_name)

                if time > last_modified:
                    self.__copy_file(path + "\\" + file_name)

            else:
                self.__iter_folder(path + "\\" + file_name, last_modified)

    def __copy_file(self, path: str) -> None:
        new_path = self.path + path[3:]
        self.total_modified += 1
        try:
            shutil.copyfile(path, new_path)

        except FileNotFoundError:
            dir_path = "\\".join(new_path.split("\\")[:-1])
            os.makedirs(dir_path)
            self.total_modified -= 1
            self.__copy_file(path)

        except Exception as e:
            self.total_modified -= 1
            print("********ERROR********")
            print(e)
            print("src:" + path)
            print("dst:" + new_path)

    def __is_connected(self, disk: str = "") -> bool:
        if disk == "":
            disk = self.path[0]
        return os.path.isdir(f"{disk}:\\")

    def __test_files_exists(self) -> bool:
        return os.path.isfile(
            self.path + ".timestamp"
        ) and os.path.isfile(self.path + ".backup")


if __name__ == "__main__":
    b = Backup()

    if len(sys.argv) <= 1:
        b.backup()
    elif sys.argv[1] in ("s", "-s", "setup", "-setup", "create", "-create"):
        b.setup()
    elif sys.argv[1] in ("a", "-a", "add", "-add"):
        b.add()
    else:
        print("Unrecognized input!")
