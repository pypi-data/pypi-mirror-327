import os.path
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))
target_file_path = os.path.join(parent_directory, "dependency")
sys.path.append(target_file_path)
