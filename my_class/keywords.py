
import os
import datefinder
import dateutil.parser as dparser
import datetime

class Keywords:
    def __init__(self, verbose, num = 5):
        self.verbose = verbose
        self.new_title = ""
        self.num = num
        self.result = []
        self.naughty_list = self.get_naughtylist()
        self.categories = self.get_category_list()
    
    def __call__(self, ocr_document):
        #pos_tag = ['PROPN', 'ADJ', 'NOUN']
        #pos_tag = ['PROPN', 'NOUN']

        ctr = 0
        chunks = list(ocr_document.noun_chunks)
        chunks = self.myfilter(chunks)
        for item in chunks: #doc.noun_chunks:
            if (ctr < self.num):
                self.new_title += str(item) + "-"
                ctr += 1
		
        #I need to filter out (most) punctuation, and replace spaces with underscores			
        if self.verbose:
            print("new_title: ", self.new_title)	

        mydate = self.get_parsed_date()
        #print("fnldate: ", str(date.date()))
        self.result = self.new_title + '[' + str(mydate.date()) + ']'
        print("new title: ", self.result)

    def get_category_list(self):
        category_file_path = os.path.join(os.getcwd(), "categories.txt")
        category_file = open(category_file_path, "r")
        categories = category_file.read().splitlines()
        category_file.close()
        return categories

    
    def get_naughtylist(self):
        naughty_file_path = os.path.join(os.getcwd(), "naughtylist.txt")
        print(naughty_file_path)
        ctr = 2
        naughty_file = open(naughty_file_path, "r")
        naughty_lines = naughty_file.read().splitlines()
        naughty_file.close()
        if self.verbose:
            print("Naughty List:", naughty_lines)
        return naughty_lines[2:]


	#this doesn't appear to be working/doing anything...
	# Get Repeats and the top few
    def myfilter(self, noun_chunks):
        nounlist = []
        chunkslist = []
        for item in noun_chunks:
            noun = str(item)
            nnoun = self.charfiltfunc(noun)
            if len(nnoun) > 2 and len(nnoun) < 30:
                if nnoun not in nounlist:
                    nounlist.append(nnoun)

        chunkslist = self.filterfunc(nounlist, naughtylist)	
        if self.verbose:
            print("New List:")
            for noun in chunkslist:
                print(noun)

        return chunkslist

    def get_parsed_date(self):
        #print("sents: \n")
        dcheck = ''
        for item in self.doc.sents:
            dcheck += str(item) + "\n\n"
        #print("dcheck: \n", dcheck)

        try:
            mydate = dparser.parse(dcheck) #  , fuzzy=True)
        except:
            dates = datefinder.find_dates(dcheck)	 #text instead of dcheck
            bestdates = []
            if self.date != '':
                year = self.date[0:3]
                mon = self.date[4:5]
                day = self.date[6:7]
                tempdate = datetime.datetime(int(year), int(mon), int(day))
                bestdates.append(tempdate)
            ctr = 0
            year = 0
            for d in dates:
                if self.verbose:
                    print("date ", d)
                
                yint = int(d.year)	
                if yint > 2015 and yint <= int(self.today.year):
                    bestdates.append(d)
                    if self.verbose:
                        print("good date: ", d)
                    #if d.year > year:
                    #	year = d.year
            if dates:
                mydate = bestdates[0]
            else:
                mydate = self.today
        return mydate

    def filterfunc(self, strlist, substrlist):
        return [tstr for tstr in strlist if not any(sub in tstr for sub in substrlist)]

    def charfiltfunc(self, tstr):
        if len(tstr) > 0:
            if tstr.find('|') != -1:
                tstr = tstr.replace('|', '', 100)
            
            if tstr.find('\n') != -1:
                tstr = tstr.replace('\n', '', 100)
            
            if tstr.find('\x0c') != -1:
                tstr = tstr.replace('\x0c', '', 100)

            if tstr.find('\\') != -1:
                tstr = tstr.replace('\\', '', 100)

            if tstr.find('.') != -1:
                tstr = tstr.replace('.', '', 100)

            if tstr.find('>') != -1:
                tstr = tstr.replace('>', '', 100)

            if tstr.find('<') != -1:
                tstr = tstr.replace('<', '', 100)

            if tstr.find('+') != -1:
                tstr = tstr.replace('+', '', 100)

            if tstr.find('=') != -1:
                tstr = tstr.replace('=', '', 100)
        
            if tstr.find(' ') != -1:
                tstr = tstr.replace(' ', '_', 100)
        
        return tstr