import sys
from pprint import pprint
from gpt4all import GPT4All

if len(sys.argv) < 2:
  print("need input")
  exit(0)
print("starting!!!\n\n\n")
pprint(sys.argv[1])
model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf", device="gpu")
# output = sys.argv[1]
no_2k = sys.argv[1].replace("[2k","")
nono_audio = no_2k.replace("[BLANK_AUDIO]", "")
output = model.generate(nono_audio, max_tokens=10000)
with open("output_gpt.txt",'w') as outfile:
  outfile.write(output)