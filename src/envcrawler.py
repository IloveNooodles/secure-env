import os

class EnvCrawler:
    def __init__(self, path: str) -> None:
        self.path = path
        self.keyval = {}
    
    def read_file(self):
        try:
          f = open(f"{self.path}", "r")
        except FileNotFoundError:
          print("File not found, exiting...")
          exit(-1)

        for line in f.readlines():
           splitted_line = line.strip().split("=")
           key, val = splitted_line[0], splitted_line[1]
           self.keyval[key] = val

        f.close()

    def write_file(self):
        f = open(f"{self.path}.enc", "w")

        for key in self.keyval:
           line = f"{key}={self.keyval[key]}\n"
           f.write(line)

        f.close()

def main():
  e = EnvCrawler("E:/secure-env/.env")
  e.read_file()
  e.write_file()

if __name__ == "__main__":
    main()