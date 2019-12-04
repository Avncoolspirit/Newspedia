import pke
import pysrt


def extract_keyword(input_line):
	# initialize keyphrase extraction model, here TopicRank
	extractor = pke.unsupervised.TopicRank()

	# load the content of the document, here document is expected to be in raw
	# format (i.e. a simple text file) and preprocessing is carried out using spacy
	extractor.load_document(input=input_line, language='en')

	# keyphrase candidate selection, in the case of TopicRank: sequences of nouns
	# and adjectives (i.e. `(Noun|Adj)*`)
	extractor.candidate_selection()

	# candidate weighting, in the case of TopicRank: using a random walk algorithm
	extractor.candidate_weighting()

	# N-best selection, keyphrases contains the 10 highest scored candidates as
	# (keyphrase, score) tuples
	keyphrases = extractor.get_n_best(n=10)
	return keyphrases


def extract_subs(file_path):
	subs = pysrt.open(file_path)
	return subs


def subs_between_time(subs,start,end):
	assert(start<end)
	output_subs = []
	for sub in subs:
 		if (int(sub.start.minutes) >= start) & (int(sub.start.minutes) <= end):
 			output_subs.append(sub.text)
	return output_subs

####Uncomment below for testing #######
# filename = input('Enter Filename :  ')
# start_time = input('Enter Start Time :  ')
# end_time = input('Enter End Time :   ')
# subs_to_extract = extract_subs(filename)

# snap = subs_between_time(subs_to_extract,int(start_time),int(end_time))
# string_test = ' '.join(snap)
# print ("These are the top Keywords for: ",extract_keyword(string_test), " For the String ", string_test)

