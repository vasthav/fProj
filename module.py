import argparse

def solver():
	print("Solve mode")

def initiator():
	print("Initiating....")

parser = argparse.ArgumentParser()
parser.add_argument("controller")
args = parser.parse_args()
if args.controller == "solve":
	solver()
elif args.controller == "initiate":
	initiator()