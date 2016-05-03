#!/usr/bin/env python

import argparse
import os
import sys


MAX_LINE_LENGTH = 88


def log(s):
  print(s)
  sys.stdout.flush()


def loge(s):
  sys.stderr.write(s + "\n")
  sys.stdout.flush()


def abort(s):
  log(s)
  sys.exit(1)


errors = []


def error(path, lineno, line, cursor, msg):
  errors.append((path, lineno, line, cursor, msg))


class Linter(object):
  def matches(self, filepath):
    abort("not implemented")

  def check(self, filepath):
    abort("not implemented")

  @staticmethod
  def check_line_length(filepath, lineno, line):
    if len(line) > MAX_LINE_LENGTH:
      msg = "Line length {0}, max {1}.".format(len(line), MAX_LINE_LENGTH)
      error(filepath, lineno, line, MAX_LINE_LENGTH, msg)


class PyLinter(object):
  def matches(self, filepath):
    return filepath.endswith(".py")

  def check(self, filepath):
    with open(filepath, "r") as f:
      lineno = 0
      for line in f:
        Linter.check_line_length(filepath, lineno, line[:-1])
        lineno += 1


class ScalaLinter(object):
  def matches(self, filepath):
    return filepath.endswith(".scala")

  def check(self, filepath):
    with open(filepath, "r") as f:
      lineno = 0
      for line in f:
        Linter.check_line_length(filepath, lineno, line[:-1])
        lineno += 1


linters = [
  PyLinter(),
  ScalaLinter()
]

def format_error(error):
  file, lineno, line, cursor, msg = error
  loge(file + ":" + str(lineno) + ": " + msg)
  loge(line)
  loge(" " * cursor + "^")


def lint(filepath):
  for linter in linters:
    if linter.matches(filepath):
      linter.check(filepath)
  for error in errors:
    format_error(error)
  if errors:
    msg = "{0} lint error{1} found.".format(
      len(errors), "" if len(errors) == 1 else "s")
    abort(msg)


def main(args):
  parser = argparse.ArgumentParser(description="Run basic lint checks.")
  parser.add_argument("-p", "--path", required=True,
    help="Path to specific file to check, or directory to check recursively.")
  args = parser.parse_args(args[1:])
  if os.path.isfile(args.path):
    lint(os.path.abspath(args.path))
  else:
    for root, dirs, files in os.walk(args.path):
      for file in files:
        lint(os.path.abspath(os.path.join(root, file)))


if __name__ == "__main__":
  main(sys.argv)
