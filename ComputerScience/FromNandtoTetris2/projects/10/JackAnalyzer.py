import sys
import os
import CompilationEngine
# import JackTokenizer

if __name__ == "__main__":
  input_path = sys.argv[1]
  suffix = ".parser.xml"

  # file / director
  if os.path.isdir(input_path):
    # directory
    files = list(filter(lambda file: file.endswith(".jack"), os.listdir(input_path)))

    if len(files) == 0:
      print("No vm file found under directory")
    else:
      for file in files:
        input_file  = os.path.join(input_path, file)
        output_file = os.path.join(input_path, file[:-5]+suffix)
        print("Processing: input_file: {} to output_file {}".format(input_file, output_file))
        CompilationEngine.CompilationEngine(input_file, output_file)
  else:
    # file
    input_file = input_path
    output_file = input_path[:-5] + suffix
    CompilationEngine.CompilationEngine(input_file, output_file)
