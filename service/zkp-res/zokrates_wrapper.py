# argv[1] is amount1
# argv[2] is random string 1
# argv[3] is amount2
# argv[4] is random string 2
import os
import sys
import hashlib
import json
import subprocess

zokrates_bin = './target/release/zokrates'

def IntToBitsArray(x, length):
  bits_array = []
  for i in range(0, length):
    bits_array=  [str(x%2)] + bits_array
    x = x/2
  return bits_array

def IntToASCIIBitsArray(x):
    bits_array = []
    s = IntToStr(x)
    for i in range(0, 32):
        bits_array.extend(IntToBitsArray(ord(s[i]), 8))
    return bits_array

#def IntToStr(x):
#  s = ''
#  for i in range(0, 32):
#    c = chr(x%256)
#    s = c + s
#    x = x/256
#  return s

def IntToStr(x):
    s = str(x)
    s = '0' * (32 - len(s)) + s
    return s

def StrToBitsArray(s):
  bits_array = []
  for c in s:
    bits_array.append(CharToBitsArray(c))
  return bits_array

def CharToBitsArray(c):
  return IntToBitsArray(ord(c), 8)

def PrepareInput():
  input_array = [sys.argv[1], sys.argv[3]]
  amount1 = int(sys.argv[1])
  amount2 = int(sys.argv[3])
  str1 = sys.argv[2][0]
  str2 = sys.argv[4][0]
  commit1 = hashlib.sha256(IntToStr(amount1) + str1).hexdigest()
  commit2 = hashlib.sha256(IntToStr(amount2) + str2).hexdigest()
  print commit1, commit2
  
  # bits array of amount1
  input_array = input_array +  IntToASCIIBitsArray(amount1)
  # bits array of random string2
  input_array = input_array + CharToBitsArray(str1)
  # bits array of amount2
  input_array = input_array +  IntToASCIIBitsArray(amount2)
  # bits array of random string2
  input_array = input_array + CharToBitsArray(str2)
  return input_array


def ParseOutput(output_file):
  result = -1
  win_bid = -1
  hash_array1 = ''
  output_dic = {}
  with open(output_file) as f:
    for line in f:
      if '~out_' in line:
        index= int(line[5: line.find(' ')])
        value = int(line[line.find(' ') +1:])
        output_dic[index] = value
  result = output_dic[0]
  win_bid = output_dic[1]
  s = ''
  for i in range(2, 66):
      s = s + (str(output_dic[i]) + ', ')
  return result, win_bid, s 

def ParseG1Point(s):
  x = s[s.find('(') + 1: s.find(',')]
  y = s[s.find(',') + 2: s.find(')')]
  return [x, y]

def ParseG2Point(s):
  s = s[s.find('(') + 1: s.find(')')]
  x1 = s[s.find('[') + 1: s.find(',')]
  y1 = s[s.find(',') + 2: s.find(']')]
  s = s[s.find(']')+2:]
  x2 = s[s.find('[') + 1: s.find(',')]
  y2 = s[s.find(',') + 2: s.find(']')]
  return [[x1, y1], [x2, y2]]

  

def GenerateProof():
  output = subprocess.check_output(
      [zokrates_bin, 'generate-proof'])
  A = []
  A_P = []
  B = []
  B_P = []
  C = []
  C_P = []
  H = []
  K = []
  for line in output[-2000:].splitlines():
   if 'A =' in line:
      A = ParseG1Point(line)
   if 'B =' in line:
      B = ParseG2Point(line)
   if 'A_p =' in line:
      A_P = ParseG1Point(line)
   if 'B_p =' in line:
      B_P = ParseG1Point(line)
   if 'C =' in line:
      C = ParseG1Point(line)
   if 'C_p =' in line:
      C_P = ParseG1Point(line)
   if 'H =' in line:
      H = ParseG1Point(line)
   if 'K =' in line:
      K = ParseG1Point(line)
  return A, A_P, B, B_P, C, C_P, H, K
 
def ComputeWitnessAndGetProof():
  input_array = PrepareInput()
  os.system(zokrates_bin + ' compute-witness -a ' + ' '.join(input_array))
  result, win_bid,s = ParseOutput('witness')
  A, A_P, B, B_P, C, C_P, H, K = GenerateProof()
  data = {'a' : A, 'a_p' : A_P, 'b' : B, 'b_p' : B_P, 'c' :C, 'c_p' : C_P,
          'h' : H, 'k' : K, 'input' : [result, win_bid]}
  json_data = json.dumps(data)
  print json_data
  

ComputeWitnessAndGetProof()
