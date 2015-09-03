import eventUtils as utils
class Document:
    ''' class for representing corpus document'''
    def __init__(self,url='',text=''):
        self.words = []
        self.sentences = []
        self.text = ''
        if url != '':
            self.URL = url.strip()
            if text == '':
                self.getText()
                if self.text == '':
                    return None
            else:
                self.text = text.strip()
        
    '''
    def __init__(self):
        self.URL = ''
        self.text = ''
        self.title = ''
        self.words = []
        self.sentences = []
    
    def __init__(self,url,text):
        self.URL = url.strip()
        self.text = text
        self.words = []
        self.sentences = []
        
    def __init__(self,url):
        self.URL = url.strip()
        self.text = ''
        self.getText()
        #self.text = ''
        self.words = []
        self.sentences = []
     '''   
    def getWords(self):
        if self.words:
            return self.words
        else:
            r = utils.getTokens(self.text)
            if len(r)>0:
                self.words = [w for w in r]
                return self.words
            else:
                return []
    
    def getText(self):
        if self.text != '':
            return self.text
        else:
            r = utils.getWebpageText(self.URL)[0]
            
            if r.has_key('text'):
                if r['text']!= '':
                    self.text = r['text']
                    self.title = r['title']
    
    def getSentences(self):
        if len(self.sentences)>0:
            return self.sentences
        else:
            if self.text:
                r = utils.getSentences(self.text)
                if len(r)>0:
                    self.sentences = [s for s in r]
                    return self.sentences
                else:
                    return []