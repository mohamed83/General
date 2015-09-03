#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys

#Variables that contains the user credentials to access Twitter API 
access_token = "248487038-zkVCyMwNiczrejIemcFHbmnj86gBbvlweIneZUmS"
access_token_secret = "08XtAoh1sTRRkc953HRCuZW5TF9zHLF4A6NdnIe5yiUDx"
consumer_key = "MMhZf1J7YRRsS9Vcy5KXYpls6"
consumer_secret = "3dGi5DOcHBX4QjmLRjnqMHjxPzgq4chk5C7HoKZCqGg5Zvo83u"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    keywords = sys.argv[1]
    #print keywords
    #stream.filter(track=['python', 'javascript', 'ruby'])
    stream.filter(track=[keywords])