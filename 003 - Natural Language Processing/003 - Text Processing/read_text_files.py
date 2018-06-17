"""Reading in text files."""
import glob, re


def read_file(filename):
    """Read a plain text file and return the contents as a string."""
    with open(filename, 'r') as f:
        text = f.read()
    return text


def read_files(path):
    """Read all files that match given path and return a dict with their contents."""
    processed_files = dict()
    files = glob.iglob(path)

    for file in files:
        file_name = re.sub(path, "", file)
        processed_files[file_name] = read_file(file)

    return processed_files

def test_run():
    # Test read_file()
    print(read_file("data/hieroglyph.txt"))

    # Test read_files()
    texts = read_files("data/*.txt")
    for name in texts:
        print("\n***", name, "***")
        print(texts[name])


if __name__ == '__main__':
    test_run()