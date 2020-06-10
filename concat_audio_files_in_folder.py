import os
import math
from pydub import AudioSegment

# directory containing files to be concatenated
rootdir = ''
# directory where the generated file will be saved
outputdir = ''
# filename for the output
outputfile = 'micromacro_concatenated.mp3'

extensions = ('.mp3', '.wav', '.aif', '.aiff', 'm4a')

timing_file_name = "timing_list.txt"
timing_file = open(os.path.join(outputdir, timing_file_name), "w")

class_list = {
	"lastnamefirstname":"Firstname Lastname",
	"lastname2firstname2":"Firstname2 Lastname2"
}

uses_crossfade = True
crossfade_duration = 1000
silence_duration = 5000

silent_buffer = AudioSegment.silent(duration=silence_duration)
output_file = AudioSegment.empty()

# number of files added 
file_counter = 0

# current time of file, used to specify start times of everyone's excerpts
current_time = 0

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.endswith(extensions):
			print("INCLUDE "+file)
			sound_file = AudioSegment.from_file(os.path.join(subdir,file))
			#normalize
			loudness_diff_file = -3 - sound_file.max_dBFS
			sound_file = sound_file.apply_gain(loudness_diff_file)
			#remove ending silence 
			sound_file_length = len(sound_file)
			silence_length = 0
			region_to_test = 0
			silence_increment = 1000

			is_silent = True

			while(is_silent):
				region_to_test -= silence_increment
				ending = sound_file[region_to_test:]
				ending_max_dbfs = ending.max_dBFS
				# if silent (or, relatively silent)
				if(ending_max_dbfs <= -45):
					silence_length = region_to_test
				else:
					is_silent = False

			sound_file_clipped_length = sound_file_length + silence_length
			sound_file = sound_file[:sound_file_clipped_length]

			name_key = file.split("_")[0]
			name = "unknown"
			if name_key in class_list:
				name = class_list[name_key]

			current_clock_time = ""
			current_minute = int(current_time/60000)
			current_second = int((current_time/1000) % 60)
			current_second_str = str(current_second)
			if current_second < 10:
				current_second_str = "0"+current_second_str

			current_clock_time = str(current_minute)+":"+current_second_str

			print(name+" "+current_clock_time)
			timing_file.write(name+" "+current_clock_time)

			if(uses_crossfade):
				if(file_counter == 0):
					output_file += sound_file
				else:
					output_file = output_file.append(sound_file, crossfade=crossfade_duration)
				current_time += sound_file_clipped_length - crossfade_duration
			else:
				if(file_counter > 0):
					output_file += silent_buffer
				output_file += sound_file
			file_counter += 1
		else:
			print("DID NOT INCLUDE "+file)

output_file.export(os.path.join(outputdir,outputfile), format="mp3")
timing_file.close()