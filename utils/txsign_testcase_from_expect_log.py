#!/usr/bin/env python3

"""Generate test vectors from expect script log.

Process log file generated by expect script to populate test vectors in user
selected output directory
"""

from os import initgroups
from pathlib import Path
import argparse

def process_expect_log(logfile):
  """Process expect script log file to get requests and responses.

  Return a pair of lists of requests and responses
  """
  requests = []
  responses = []
  request_marker = "Please scan the QR-Code using the red scanner"
  response_marker = "Displaying QR code. Data: "
  with open(logfile, 'r') as f:
    lines = f.readlines()
    for i in range(0, len(lines)):
      if lines[i].startswith(request_marker):
        requests.append(lines[i+1].strip())
        i = i + 1
      elif lines[i].startswith(response_marker):
        responses.append(lines[i][len(response_marker) : ].strip())      
  assert len(requests) == len(responses), "Number of requests does not match number of responses"
  return (requests, responses)

def generate_test_vectors_from_expect_log(logfile, out_dir, is_qr=False):
  """Generate test vectors from expect log, and write them to files.

  All test vectors are written into files in out_dir.
  """
  requests, responses = process_expect_log(logfile)
  for i, (req, res) in enumerate(zip(requests, responses)):
    
    filePath = Path(out_dir) / "valid-{}{:0>4d}".format("qr" if is_qr else "",i)

    with open(filePath, "w") as f:
      f.writelines(["request:" + req, "\n", "response:" + res, "\n"])

  print("{0} test cases written to {1}".format(len(requests), out_dir))

if __name__ == "__main__":
  parser = argparse.ArgumentParser("Create subzero txsign test vectors from a log file")
  parser.add_argument("-o", "--out_dir", nargs=1, help="output directory for test vectors", required=True)
  parser.add_argument("-i", "--input_log", nargs=1, help="input log file from expect script", required=True)
  parser.add_argument("--qrsigner", help="generated test vectors for qr signing", action='store_true')

  args = parser.parse_args()
  logfile = args.input_log[0]
  out_dir = args.out_dir[0]
  generate_test_vectors_from_expect_log(logfile, out_dir, args.qrsigner)
