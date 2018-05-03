import facebook_james

def main():
    print "Analysis of posts from IBM's Facebook"
    facebook_james.printPosts()
    facebook_james.getLexicalDiversity()
    
main()