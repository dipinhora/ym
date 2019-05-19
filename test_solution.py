class Contact:
  def __init__(self, name, phone, email):
    self.name = name
    self.phone = phone
    self.email = email

  def __repr__(self):
    return "<Contact name:%s phone:%s email:%s>" % (self.name, self.phone, self.email)

  def __lt__(self, other):
    # define less than based on object id since we only need ordering to be
    # consistent and not based on any specific value of the object
    # NOTE: this is only needed for unordered testing of the lists; if
    # reliable sorting of contacts were really needed for a business purpose,
    # using "id" almost definitely wouldn't be appropriate
    return id(self) < id(other)


def mergeUsers(contacts):
  # dictionary for checking matches based on phone and email
  dict = {}

  # iterate all contacts
  for c in contacts:
    # check if the there's already a list of contacts by this contact's phone
    phone_entry = dict.get(c.phone)

    # check if the there's already a list of contacts by this contact's email
    email_entry = dict.get(c.email)

    # if neither phone or email has been seen previously
    if phone_entry is None and email_entry is None:
      # create a new list holding this contact
      l = [ c ]

      # add dictionary entries for this contact's email and phone holding the new list
      dict[c.email] = l
      dict[c.phone] = l

    # if match by email
    if phone_entry is None and email_entry is not None:
      # append contact to email list
      email_entry.append(c)

      # add dictionary entry for this contact's phone pointing to the email_entry
      dict[c.phone] = email_entry

    # if match by phone
    if phone_entry is not None and email_entry is None:
      # append contact to phone list
      phone_entry.append(c)

      # add dictionary entry for this contact's email pointing to the phone_entry
      dict[c.email] = phone_entry

    # if match by phone and email
    if phone_entry is not None and email_entry is not None:
      # if both phone and email dict entries point to the same list
      if phone_entry == email_entry:
        # append contact to the list
        phone_entry.append(c)
      # if phone and email dict entries point to different list
      else:
        # append contact to the phone entry list
        phone_entry.append(c)
        # append all email list entries to the phont entry list
        phone_entry.extend(email_entry)
        # overwrite the dict entres from email_entry with phone_entry
        dict[c.email] = phone_entry
        for c in email_entry:
          # if contact's phone entry points to email_entry overwrite with phone_entry
          if dict[c.phone] == email_entry:
            dict[c.phone] = phone_entry
          # if contact's email entry points to email_entry overwrite with phone_entry
          if dict[c.email] == email_entry:
            dict[c.email] = phone_entry

  # create output list of lists
  o = []
  # for each list pointed to by any dict entry
  for v in dict.values():
    # if it's not already in the output list
    if v not in o:
      # add to the output list
      o.append(v)

  # return the output list of lists
  return o


import numpy as np

def doesWordExist(grid, word):
  # get the first letter
  first_letter = word[0]
  # find all occurrences of the first letter
  found = np.where(grid == first_letter)

  # for every occurence of the first letter
  for x in range(0, found[0].size):
    # get offsets for instance of first letter
    current_pos = (found[0][x], found[1][x])

    # check for word using recursive depth first search function
    if find_word(grid, word, current_pos, 0, [ ]):
      return True

  # didn't find the word
  return False

# recursive depth first search function
def find_word(grid, word, current_pos, letter_num, seen_pos):
  # if we've seen this position already, it's not found
  if current_pos in seen_pos:
    return False

  current_letter = word[letter_num]
  xpos = current_pos[0]
  ypos = current_pos[1]

  # if the current grid position doesn't match the letter, it's not found
  if grid[xpos][ypos] != current_letter:
    return False

  # if we've matched all the letters of the word, it's found
  if letter_num + 1 == len(word):
    return True

  new_seen_pos = seen_pos + [ current_pos ]
  (xsize, ysize) = grid.shape

  # check each direction to continue matching the word
  if find_word(grid, word, ((xpos + 1) % xsize, ypos), letter_num + 1, new_seen_pos):
    return True

  if find_word(grid, word, (xpos - 1, ypos), letter_num + 1, new_seen_pos):
    return True

  if find_word(grid, word, (xpos, (ypos + 1) % ysize), letter_num + 1, new_seen_pos):
    return True

  if find_word(grid, word, (xpos, ypos - 1), letter_num + 1, new_seen_pos):
    return True

  # didn't find the word
  return False










class TestMergeUsers(object):
  def test_match_simple(self):
    mrx = Contact('Mr. X', '123-456-7890', 'x@yieldmo.com')
    msy = Contact('Ms. Y', '456-789-1234', 'y@yieldmo.com')
    mrx1 = Contact('Mr. X1', '123-456-7890', 'x@gmail.com')
    msy1 = Contact('Ms. Y1', '456-789-9999', 'y@yieldmo.com')
    mrz = Contact('Mr. Z', '123-654-7890', 'z@yieldmo.com')
    i = [ mrx, msy, mrx1, msy1, mrz ]
    o = [ [ mrx, mrx1 ], [ msy, msy1 ], [ mrz ] ]
    r = mergeUsers(i)
    # make sure to sort before comparing because normal equality assert is
    # sensitive to ordering
    assert all([ sorted(a) == sorted(b) for a, b in zip(sorted(o), sorted(r)) ])

  def test_match_simple_with_duplicate(self):
    mrx = Contact('Mr. X', '123-456-7890', 'x@yieldmo.com')
    mrx_dupe = Contact('Mr. X', '123-456-7890', 'x@yieldmo.com')
    msy = Contact('Ms. Y', '456-789-1234', 'y@yieldmo.com')
    mrx1 = Contact('Mr. X1', '123-456-7890', 'x@gmail.com')
    msy1 = Contact('Ms. Y1', '456-789-9999', 'y@yieldmo.com')
    mrz = Contact('Mr. Z', '123-654-7890', 'z@yieldmo.com')
    i = [ mrx, msy, mrx1, msy1, mrz, mrx_dupe ]
    o = [ [ mrx, mrx1, mrx_dupe ], [ msy, msy1 ], [ mrz ] ]
    r = mergeUsers(i)
    # make sure to sort before comparing because normal equality assert is
    # sensitive to ordering
    assert all([ sorted(a) == sorted(b) for a, b in zip(sorted(o), sorted(r)) ])

  def test_match_complex(self):
    mrx = Contact('Mr. X', '123-456-7890', 'x@yieldmo.com')
    msy = Contact('Ms. Y', '456-789-1234', 'y@yieldmo.com')
    mrx1 = Contact('Mr. X1', '123-456-7890', 'x@gmail.com')
    msy1 = Contact('Ms. Y1', '456-789-9999', 'y@yieldmo.com')
    mrz = Contact('Mr. Z', '123-456-7890', 'z@yieldmo.com')
    mrz1 = Contact('Mr. Z1', '456-789-9999', 'z@yieldmo.com')
    i = [ mrx, msy, mrx1, msy1, mrz, mrz1 ]
    o = [ [ mrx, mrx1, msy, msy1, mrz, mrz1 ] ]
    r = mergeUsers(i)
    # make sure to sort before comparing because normal equality assert is
    # sensitive to ordering
    assert all([ sorted(a) == sorted(b) for a, b in zip(sorted(o), sorted(r)) ])

class TestDoesWordExist(object):
  def test_match_right(self):
    word = "mop"
    grid = np.array([ ['a','c','d','e','f']
                     ,['g','h','i','j','e']
                     ,['o','p','q','u','m']
                     ,['s','w','t','u','v'] ])

    assert doesWordExist(grid, word)

  def test_no_match(self):
    word = "zop"
    grid = np.array([ ['a','c','d','e','f']
                     ,['g','h','i','j','e']
                     ,['m','o','p','q','u']
                     ,['s','w','t','u','v'] ])

    assert not doesWordExist(grid, word)

  def test_match_left(self):
    word = "cafe"
    grid = np.array([ ['a','c','d','e','f']
                     ,['g','h','i','j','c']
                     ,['m','o','p','q','u']
                     ,['s','w','t','u','v'] ])

    assert doesWordExist(grid, word)

  def test_match_up(self):
    word = "gas"
    grid = np.array([ ['a','c','d','e','f']
                     ,['g','h','i','j','e']
                     ,['m','o','p','q','u']
                     ,['s','w','t','u','v'] ])

    assert doesWordExist(grid, word)

  def test_match_down(self):
    word = "sag"
    grid = np.array([ ['a','c','d','e','f']
                     ,['g','h','i','j','e']
                     ,['m','o','p','q','u']
                     ,['s','w','t','u','v'] ])

    assert doesWordExist(grid, word)

  def test_nomatch_repeat(self):
    word = "pop"
    grid = np.array([ ['a','c','d','e','f']
                     ,['g','h','i','j','e']
                     ,['m','o','p','q','u']
                     ,['s','w','t','u','v'] ])

    assert not doesWordExist(grid, word)

  def test_match_directions(self):
    word = "sesquipedalian"
    grid = np.array([ ['e','d','e','n','s']
                     ,['s','e','j','e','q']
                     ,['i','p','q','f','u']
                     ,['l','a','u','a','i'] ])

    assert doesWordExist(grid, word)
