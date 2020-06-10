import os
from pydub import AudioSegment

source_filepath = ''
output_filepath = ''

sound_file = AudioSegment.from_file(source_filepath)
sound_file_length = len(sound_file)
silence_length = 0
region_to_test = 0
silence_increment = 1000

is_silent = True

while(is_silent):
	region_to_test -= silence_increment
	ending = sound_file[region_to_test:]
	ending_max_dbfs = ending.max_dBFS
	# if silent
	if(ending_max_dbfs <= -45):
		silence_length = region_to_test
	else:
		is_silent = False

sound_file_clipped_length = sound_file_length + silence_length
sound_file_clipped = sound_file[:sound_file_clipped_length]

sound_file_clipped.export(output_filepath)