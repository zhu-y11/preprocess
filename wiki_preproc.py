# -*- coding: UTF-8 -*-
#!/usr/bin/python3
"""
Preprocessing wiki text
@Author Yi Zhu
Upated  30/11/2017
"""

#************************************************************
# Imported Libraries
#************************************************************
import os
import re
import argparse
from tqdm import tqdm
import string

"""
import polyglot
from polyglot.text import Text, Word
from polyglot.tokenize import SentenceTokenizer
from polyglot.base import Sequence
"""

from nltk.tokenize import sent_tokenize
from nltk.tokenize.moses import MosesTokenizer

from lang_map import lang_map


def main(args):
  full_lang = args.lang
  lang = lang_map[full_lang]
  for root, dirs, files in tqdm(os.walk(args.input_dir), total = len(os.listdir(args.input_dir))):
    for file_name in tqdm(files, total = len(os.listdir(root))):
      # input file
      in_file = os.path.join(root, file_name)
      # create the same dir in output_dir
      rel_in_path = os.path.dirname(os.path.relpath(in_file, args.input_dir))
      if not os.path.exists(os.path.join(args.output_dir, rel_in_path)):
        os.makedirs(os.path.join(args.output_dir, rel_in_path))

      with open(in_file, 'r') as f, open(os.path.join(args.output_dir, rel_in_path, file_name), 'w') as f1:
        docs = f.read().strip().split('</doc>')
        # delete documents with only title
        docs = [doc.strip() for doc in docs if doc.strip().count('\n') > 1]
        # discard the head
        docs = [doc[doc.find('\n') + 1:] for doc in docs]
        for doc in docs:
          pars = doc.strip().split('\n')
          # discard the title
          pars = [par.strip() for par in pars if par.strip()][1:]
          new_pars = []
          for par in pars:
            sents = sentSegment(par, full_lang)
            new_sents = []
            for sent in sents:
              try:
                words = wordTokenize(sent, lang)
              except:
                continue
              # delete punctuations
              words = [word for word in words if word not in string.punctuation]
              # delete sentence with only one word
              if len(words) <= 1:
                continue
              new_sent = ' '.join(words)
              new_sent = repMultiDigits(new_sent)
              new_sent = new_sent.lower()
              new_sents.append(new_sent)
            if not new_sents:
              continue
            new_pars.append('\n'.join(new_sents))
          if not new_sents:
            continue
          new_doc = '\n\n'.join(new_pars)
          f1.write(new_doc + '\n' * 5)


def sentSegment(par, lang):
  sents = sent_tokenize(par, lang)
  return sents


def wordTokenize(sent, lang):
  tokenizer = MosesTokenizer(lang)
  words = tokenizer.tokenize(sent, escape = False)
  return words


def repMultiDigits(tok_text):
  regex_list = [ r'[+-]?(\d+[\,\.]\d+)([eE][+-]?\d+)?', r'\d+']
  for reg in regex_list:
    tok_text = re.sub(reg, '#', tok_text)
  return tok_text


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = 'Pre-processing for wiki text after extraction')
  parser.add_argument('input_dir', help = 'input dir')
  parser.add_argument('-o', '--output_dir', default = 'text',
                      help = 'output dir')
  parser.add_argument('--lang', default = 'it',
                      help = 'language for preprocessing')
  args = parser.parse_args()
  main(args)
