#!/usr/bin/env python3

"""
Takes a list of collection IDs as arguments, and prints a TSV
(name, ids) containing names with same name but different ids i.e. authors with 
same name.

Place in acl-anthology/bin and run

   ./bin/ambiguous-names.py 2020.acl
   
which prints all authors with same full name but different id.
These names are the ambiguous names. 

Author: Sharmila Upadhyaya
"""

import os
import sys

from anthology import Anthology
from anthology.people import PersonName
from anthology.utils import deconstruct_anthology_id

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("collections", nargs="+")
  args = parser.parse_args()

  anthology = Anthology(importdir=os.path.join(os.path.dirname(sys.argv[0]), "..", "data"))

  # header
  print("Name", "IDs", sep="\t\t\t")
  authors_name = anthology.people
  for key, value in authors_name.name_to_ids.items():

      if len(value)>1:
         print(key,", ".join(value ), sep = "\t\t\t")
            
