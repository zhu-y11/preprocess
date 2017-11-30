# -*- coding: UTF-8 -*-
#!/usr/bin/python3
"""
Convert input format of Wiki data for different model
@Author Yi Zhu
Upated 25/11/2017
"""

#************************************************************
# Imported Libraries
#************************************************************
import argparse
from tqdm import tqdm
import os


def main(args):
  conv2SentSplit(args)
  #conv2DocSplit(args)
  

def conv2SentSplit(args):
  with open(args.output_file + '.sent', 'w') as f1:
    for root, dirs, files in tqdm(os.walk(args.input_dir), total = len(os.listdir(args.input_dir))):
      for file_name in files:
        # input file
        in_file = os.path.join(root, file_name)

        with open(in_file, 'r') as f:
          docs = f.read().strip().split('\n' * 4)
          docs = [doc.strip().split('\n\n') for doc in docs]
          docs = ['\n'.join(doc) for doc in docs]
          f1.write('\n'.join(docs) + '\n')


def conv2DocSplit(args):
  with open(args.output_file + '.doc', 'w') as f1:
    for root, dirs, files in tqdm(os.walk(args.input_dir), total = len(os.listdir(args.input_dir))):
      for file_name in files:
        # input file
        in_file = os.path.join(root, file_name)

        with open(in_file, 'r') as f:
          docs = f.read().strip().split('\n' * 4)
          for i, doc in enumerate(docs[:]):
            sents = doc.strip().split('\n')
            sents = [sent.strip() for sent in sents if sent.strip()]
            docs[i] = ' '.join(sents)
          f1.write('\n'.join(docs) + '\n')


if __name__ == '__main__':
  parser = argparse.ArgumentParser('Input Conversion')
  parser.add_argument('-m', '--model', default = 'word2vec',
                      help = 'word embedding model')
  parser.add_argument('-i', '--input_dir', required = True,
                      help = 'input wiki data dir')
  parser.add_argument('-o', '--output_file', default = 'corpus',
                      help = 'output wiki data file')
  args = parser.parse_args()
  main(args)
