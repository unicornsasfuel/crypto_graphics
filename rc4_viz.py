from time import sleep

def visualize(state, prev_state):
   '''Pretty prints the state of RC4. Green indicates values
   that have not changed, red indicates values that have
   changed.'''
   output = ''
   length = len(state)
   if length != len(prev_state):
      return False

   for i in range(length):
      if i % 16 == 0:
         output += '\n'
      if state[i] == prev_state[i]:
         output += '[' + greentext(ord(state[i])) + ']'
      else:
         output += '[' + redtext(ord(state[i])) + ']'

   print output
   sleep(1)


def greentext(byte):
   return '\033[1;32m{0:02x}\033[1;m'.format(byte)


def redtext(byte):
   return '\033[1;31m{0:02x}\033[1;m'.format(byte)


def ksa(key, viz=False):
   '''Key Scheduling Algorithm of RC4
   key: The secret key
   '''
   length = len(key)
   j = 0
   state = [0] * 256

   for i in range(256):
      state[i] = chr(i)
   if viz:
      print 'initial state'
      visualize(state, state) # no previous state, use state for prev_state
   for i in range(256):
      j = ( j + ord(state[i]) + ord(key[i % length]) ) % 256
      if viz:
         prev_state = state[:] # slice to get a copy instead of a reference
      t = state[i]
      state[i] = state[j]
      state[j] = t
      if viz:
         print '\nswap S[i] and S[j]'
         visualize(state, prev_state)

   return state


def prga(key, length, viz=False):
   '''The PseudoRandom Generator Algorithm of RC4
   key: The secret key
   length: The number of bytes to generate
   viz: Whether or not to visualize the state
   '''
   i = j = 0
   output = ''
   state = ksa(key, viz)

   for junk_var in range(length):
      i = (i + 1) % 256
      j = (j + ord(state[i])) % 256
      t = state[i]
      state[i] = state[j]
      state[j] = t
      output += state[(ord(state[i]) + ord(state[j])) % 256]

   return output

prga('flibbledibbz', 10, viz=True)
