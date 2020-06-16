from pathlib import Path
import sys

class Site():
    """ The site class """
    def __init__(self, source: Path, dest: Path, parsers=None):
        """ Intialise with source and dest """
        self.source = Path(source)
        self.dest = Path(dest)
        self.parsers = parsers or []
    
    def create_dir(self,path: Path):
        """ Creates directory at path"""
        directory = self.dest / path.relative_to(self.source)
        directory.mkdir(parents=True, exist_ok=True)
    
    def build(self):
        self.dest.mkdir(parents=True, exist_ok=True)
        for path in self.source.rglob("*"):
            if path.is_dir():
                try:
                    self.create_dir(path)
                except:
                    print("error build")
            elif path.is_file():
                try:
                    self.run_parser(path)
                except:
                    print("error")
                    
    def load_parser(self, extension):
        for parser in self.parsers:
            if parser.valid_extension(extension):
                return parser
    
    def run_parser(self, path: Path):
        parser = self.load_parser(path.suffix)
        if parser is not None:
            parser.parse(path,self.source, self.dest)
        else:
            self.error("No parser for the {} extension, file skipped!".format(path.suffix))
    
    @staticmethod
    def error(message):
        sys.stderr.write("\x1b[1;31m{}\n".format(message))