import os
from pydub import AudioSegment

# directory containing source files 
rootdir = ''
# output file directory
outputdir = ''
# output file name 
outputfile = 'micromacro_overlaid.mp3'

extensions = ('.mp3', '.wav', '.aif', '.aiff', 'm4a')

# number of files added 
file_counter = 0
# total number of files 
total_file_count = 0
# max file length
overall_file_length = 0

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.endswith(extensions):
			print("INCLUDING "+file)
			sound_file = AudioSegment.from_file(os.path.join(subdir,file))
			sound_file_duration = len(sound_file)
			if(sound_file_duration > overall_file_length):
				overall_file_length = sound_file_duration
			file_counter += 1
		else:
			print("DID NOT INCLUDE "+file)

total_file_count = file_counter
file_counter = 0

print("overall duration is "+str(overall_file_length)+" ms")
print("total number of files: "+str(total_file_count))

output_file = AudioSegment.silent(duration=overall_file_length)

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.endswith(extensions):
			print("OVERLAYING "+file)
			sound_file = AudioSegment.from_file(os.path.join(subdir,file))
			#normalize
			loudness_diff_file = -3 - sound_file.max_dBFS
			sound_file = sound_file.apply_gain(loudness_diff_file)
			sound_file_duration = len(sound_file)
			sound_file_index_pct = file_counter / float(total_file_count)
			print("file count: "+str(file_counter))
			print("file index pct: "+str(sound_file_index_pct))
			duration_difference = overall_file_length - sound_file_duration
			time_offset = duration_difference * sound_file_index_pct
			print("time offset: "+str(time_offset))
			output_file = output_file.overlay(sound_file, position=time_offset)
			file_counter += 1

loudness_difference = -3 - output_file.max_dBFS
output_file = output_file.apply_gain(loudness_difference)

output_file.export(os.path.join(outputdir,outputfile), format="mp3")