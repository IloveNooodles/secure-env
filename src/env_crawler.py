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

    def get_key_val(self):
        return self.keyval
      
    def set_key_val(self, new_key_val):
        self.keyval = new_key_val

    def write_file(self, decrypt=False):
        if decrypt:
          path = self.path.split(".enc")
          f = open(path[0], "w")
        else:
          f = open(f"{self.path}.enc", "w")

        for key in self.keyval:
           line = f"{key}={self.keyval[key]}\n"
           try:
              f.write(line)
           except:
              print("Wrong password, decryption failed")

        f.close()

def main():
  e = EnvCrawler("E:/secure-env/.env")
  e.read_file()
  e.write_file()

if __name__ == "__main__":
    main()