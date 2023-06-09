import re

"""Extracts song, artist pairs from a string."""
def extract_song_artist_pairs(response):
  song_artist_pairs = []

  output_string = response[response.find("1."):] 
  # print(output_string)
  lines = output_string.split('\n')
  # print(lines)

  # Iterate over the lines.
  for line in lines:
    # Match the song and artist in the line.
    match = re.match(r'^(.+), (.+)$', line)

    # if not match:
    #   print(line)
    #   match = re.match(r'^(\d+)\. "(.+)" by (.+)$', line)
    #   print("after")
    #   print(match)

    if match:
      song_artist_pairs.append(strip_numbers((match.group(1), match.group(2))))

  return song_artist_pairs

"""Strips numbers from a list of elements."""
def strip_numbers(elements):
  stripped_elements = []

  for element in elements:
    # Strip the number from the element.
    element = re.sub(r'^\d+\. ', '', element)

    stripped_elements.append(element)

  return stripped_elements

# print(extract_song_artist_pairs("Final Answer: 1. 'Birds' by Imagine Dragons \n2. 'River' by Leon Bridges \n3. 'Woods' by Bon Iver"))