#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019--2021 Matt Post <post@cs.jhu.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This program takes one or more XML files as arguments.
- Reads through each file and does the following:
- Finds all papers with one author and adds "Matt POST" as a coauthor
- Finds all papers with more than two authors, and removes authors 3+
- Transforms each author's last name (surname / family name) to ALL CAPS
Writes out the XML file back to disk

"""

import argparse
import os
import re
import readline
import shutil
import sys

import lxml.etree as etree

from collections import defaultdict, OrderedDict
from datetime import datetime

from normalize_anth import normalize
from anthology.utils import (
    make_simple_element,
    build_anthology_id,
    deconstruct_anthology_id,
    indent,
    compute_hash_from_file,
)
from anthology.index import AnthologyIndex
from anthology.people import PersonName
from anthology.bibtex import read_bibtex
from anthology.venues import VenueIndex

from itertools import chain
from typing import Dict, Any


def main(args):
    for collection_file in args.files:
        root_node = etree.parse(collection_file).getroot()
        for paper in root_node.findall(".//paper"):
            authors = paper.findall("./author")

            if len(authors) == 1:
                author_root = etree.Element('author')
                etree.SubElement(author_root,"first").text = "Matt"
                etree.SubElement(author_root,"last").text = "POST"
                authors[0].addnext(author_root)


            elif len(authors) > 2:
                for each_author in authors[2:]:
                    paper.remove(each_author)

            for author in authors[:2]:
                a = author.find("./last")
                a.text = a.text.upper()

        tree = etree.ElementTree(root_node)
        indent(root_node)
        tree.write(
            collection_file, encoding="UTF-8", xml_declaration=True, with_tail=True
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="List of XML files.")
    args = parser.parse_args()
    main(args)
