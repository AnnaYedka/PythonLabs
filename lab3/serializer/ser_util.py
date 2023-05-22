import argparse

from serializer.serializer import Serializer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="JSON&XMLserialiser")
    parser.add_argument("file_from", help="file from which data is loaded")
    parser.add_argument("file_to",  help="file to which serialized data is saved")
    parser.add_argument("format_from", choices=["json", "xml"], help="format from which data is deserialized")
    parser.add_argument("format_to", choices=["json", "xml"], help="format to which data is serialized")

    args = parser.parse_args()
    s_from = Serializer.create_serializer(args.format_from)
    s_to = Serializer.create_serializer(args.format_to)
    s_to.dump(s_from.load(args.file_from), args.file_to)