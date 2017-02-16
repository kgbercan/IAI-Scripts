# This script goes through sound and TextGrid files in a directory,
# opens each pair of Sound and TextGrid, notes the time of a variety of points placed on two tiers, one for segments, and one for tones,
# finds the F0 at those points, does some other stuff too, and then saves results to a text file.
#
# This script was originally distributed under the GNU General Public License.
# Copyright 4.7.2003 Mietta Lennes
# Later modified extensively by John Bates, and then possibly even more extensively by Jon Barnes.
# and still later, modified slightly by Nanette Veilleux (Jan 2012) 

form Analyze pitch from labeled points in files
	comment Directory of sound files
	text sound_directory  /Users/Karina/Documents/CREU/Spring2017_recordings/P2 copy/
	sentence Sound_file_extension .wav
	comment Directory of TextGrid files
	text textGrid_directory  /Users/Karina/Documents/CREU/Spring2017_recordings/P2 copy/
	sentence TextGrid_file_extension .TextGrid
	comment Full path of the resulting text file:
	text resultfile /Users/Karina/Documents/CREU/Spring2017_recordings/P2 copy/results.txt
	comment Which tier contains the speech sound segments?
	sentence Phone_tier segments
	comment Which tier contains the syllable segments?
	sentence Tone_tier f0
	comment Pitch analysis parameters
	positive Time_step 0.01
	positive Minimum_pitch_(Hz) 75
	positive Maximum_pitch_(Hz) 550
endform

# Here, you make a listing of all the sound files in a directory.
# The example gets file names ending with ".wav" from wherever you told it to look.

Create Strings as file list... list 'sound_directory$'*'sound_file_extension$'
numberOfFiles = Get number of strings

# Check to see if the result file exists:
if fileReadable (resultfile$)
	pause The result file 'resultfile$' already exists! Do you want to overwrite it?
	filedelete 'resultfile$'
endif

# Write a row with column titles to the result file:
# (remember to edit this if you add or change the analyses!)

titleline$ = "filename	oc_time	oc_f0	bv_time	bv_f0	bc_time	bc_f0	es_time	es_f0	meanf0_accsyll	l_time	l_f0	h_time	h_f0	tcog	tcog_percsyll	tcog_to_vmid	l_to_bv	h_to_bc	l_perc	h_perc	vdur	tcog_to_bv'newline$'"
fileappend "'resultfile$'" 'titleline$'

for ifile to numberOfFiles
	filename$ = Get string... ifile
	# A sound file is opened from the listing:
	Read from file... 'sound_directory$''filename$'
	# Starting from here, you can add everything that should be 
	# repeated for every sound file that was opened:
	soundname$ = selected$ ("Sound", 1)
	To Pitch... time_step minimum_pitch maximum_pitch
	# Open a TextGrid by the same name:
	gridfile$ = "'textGrid_directory$''soundname$''textGrid_file_extension$'"
	if fileReadable (gridfile$)
		Read from file... 'gridfile$'
		# Find the tier number that has the label given in the form:
		call GetTier 'phone_tier$' phone_tier
		call GetTier 'tone_tier$' tone_tier

# set variables to zero
		oc = 0
		pitchoc = 0
		bv = 0
		pitchbv = 0
		bc = 0
		pitchbc = 0
		es = 0
		pitches = 0
		meanf0syl = 0
		l = 0
		pitchl = 0
		h = 0
		pitchh = 0
		tcog = 0
		tcog_to_vmid = 0
		tcog_percsyll = 0
		l_to_bv = 0
		h_to_bc = 0
		l_perc = 0
		h_perc = 0
		vdur = 0
		tcog_to_bv = 0

		# extract the times and f0 for lables on phone tier (oc,bv,bc,es)
		numberOfPointsphone = Get number of points... phone_tier
		for point to numberOfPointsphone
			label$ = Get label of point... phone_tier point
				
			if label$ = "oc" or label$ = "oc?"
				oc = Get time of point... phone_tier point
				select Pitch 'soundname$'
				pitchoc = Get value at time... oc Hertz Linear
				select TextGrid 'soundname$'
			endif

			if label$ = "bv" or label$ = "bv?"
				bv = Get time of point... phone_tier point
				select Pitch 'soundname$'
				pitchbv = Get value at time... bv Hertz Linear
				select TextGrid 'soundname$'
			endif
			
				
			if label$ = "bc" or label$ = "bc?"
				bc = Get time of point... phone_tier point
				select Pitch 'soundname$'
				pitchbc = Get value at time... bc Hertz Linear
				select TextGrid 'soundname$'
			endif

			if label$ = "es" or label$ = "es?"
				es = Get time of point... phone_tier point
				select Pitch 'soundname$'
				pitches = Get value at time... es Hertz Linear
				select TextGrid 'soundname$'
			endif
				
		endfor

	#Get the mean pitch during the accented syllable [bv,es]
		select Pitch 'soundname$'
		meanf0syll = Get mean... bv es Hertz
		select TextGrid 'soundname$'

	#Now work through the tone (f0) tier, doing the same thing as above on the phone...(l,h)
	# l is the low before the initial rise and h is the maximum
			numberOfPointstone = Get number of points... tone_tier
			for point to numberOfPointstone
				label$ = Get label of point... tone_tier point
				if label$ = "l"
					l = Get time of point... tone_tier point
					select Pitch 'soundname$'
					pitchl = Get value at time... l Hertz Linear
					select TextGrid 'soundname$'
				endif
			
				if label$ = "h" or label$ = "h?"
					h = Get time of point... tone_tier point
					select Pitch 'soundname$'
					pitchh = Get value at time... h Hertz Linear
					select TextGrid 'soundname$'
				endif
			endfor

	# Now get the TCoG time of whatever interval you are interested in

		select Pitch 'soundname$'
		
		# get local [bv,es] min as baseline, max and range and convert to semitones 
		baseline_Hz = Get minimum... bv es Hertz Parabolic
		baseline = 39.863 * ( ln (baseline_Hz) / ln (10) )
		f0Max_Hz = Get maximum... bv es Hertz Parabolic
		f0Max = 39.863 * ( ln (f0Max_Hz) / ln (10) )
		f0Range = f0Max - baseline
		
		#get the beginning time point: the minimum from bv to h (prob not be baseline time)
		leftedge = Get time of minimum... bv h Hertz Parabolic
		printline 'leftedge'

		start = Get start time
		end = Get end time
		Down to PitchTier
			Remove points between... start leftedge
			Remove points between... es end
		Down to TableOfReal... Hertz

		# table of reals has two columns: time (col 1), f0 (col 2) 
		sumProd = 0
		sumWeight = 0
		nrow = Get number of rows
		for i  to nrow
			# col1 has the time
			time = Get value... i 1
			# col2 has the f0 in Hz
			f0Hz = Get value... i 2
			f0 = 39.863 * ( ln (f0Hz) / ln (10) )
			#f0Norm is the f0  - baseline / range
			f0Norm = (f0 - baseline)/(f0Range)	
			#sigmatize the f0 in hz
			sigmoid01 = 1000/(998*(1+exp(-6.9*(2*f0Norm - 1)))) - 0.001
			prod = time * sigmoid01
			sumProd += prod

			sumWeight += sigmoid01
			#sumWeight +=f0minusbase
		
		endfor

		tcog = sumProd/sumWeight
		tcog_percsyll = (tcog - bv)/(es-bv)
		tcog_to_vmid = tcog - ((bc+ bv)/2)
		select TextGrid 'soundname$'

		Insert point... tone_tier tcog TCoG

		filedelete "'gridfile$'"
		Write to text file... 'sound_directory$''soundname$'.TextGrid

		l_to_bv = l - bv
		h_to_es = h - es
		l_perc = (l - bv)/(es-bv)
		h_perc = (h - bv)/(es-bv) 
		vdur = bc - bv
		if bc = 0
			vdur = es-bv
		endif
		tcog_to_bv = tcog - bv
		

	# Save result to text file:
		resultline$ = "'soundname$'	'oc'	'pitchoc'	'bv'	'pitchbv'	'bc'	'pitchbc'	'es'	'pitches'	'meanf0syll'	'l'	'pitchl'	'h'	'pitchh'	'tcog'	'tcog_percsyll'	'tcog_to_vmid'	'l_to_bv'	'h_to_bc'	'l_perc'	'h_perc'	'vdur'	'tcog_to_bv''newline$'"
		fileappend "'resultfile$'" 'resultline$'

	

	# Remove intermediate objects from object window
		select TableOfReal 'soundname$'
			Remove
		select PitchTier 'soundname$'
			Remove
		select Pitch 'soundname$'
			Remove

	# Remove the TextGrid object from the object list
		select TextGrid 'soundname$'
			Remove
endif
	
# Remove the sound object from the object list
	select Sound 'soundname$'
		Remove
	select Strings list
	# and go on with the next sound file!
endfor

Remove
	

#-------------
# This procedure finds the number of a tier that has a given label.

procedure GetTier name$ variable$
        numberOfTiers = Get number of tiers
        itier = 1
        repeat
                tier$ = Get tier name... itier
                itier = itier + 1
        until tier$ = name$ or itier > numberOfTiers
        if tier$ <> name$
                'variable$' = 0
        else
                'variable$' = itier - 1
        endif

	if 'variable$' = 0
		exit The tier called 'name$' is missing from the file 'soundname$'!
	endif

endproc
