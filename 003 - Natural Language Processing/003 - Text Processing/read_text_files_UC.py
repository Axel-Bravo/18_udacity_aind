"""Reading in text files."""


def read_file(filename):
    """Read a plain text file and return the contents as a string."""
    pass  # TODO: Open "filename", read text and return it


def read_files(path):
    """Read all files that match given path and return a dict with their contents."""

    # TODO: Get a list of all files that match path (hint: use glob)

    # TODO: Read each file using read_file()

    # TODO: Store & return a dict of the form { <filename>: <contents> }
    # Note: <filename> is just the filename (e.g. "hieroglyph.txt") not the full path ("data/hieroglyph.txt")

    pass


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