import bigrams
import facebook_james
import website_summary
import pos_analysis

def main():
    print "Analysis of tweets from Starbucks"
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
    tw = twitter.Twitter(auth=auth)
    get_tweets(tw)
    print "*" * 30 + 'END' + "*" * 30 
    
    print "Analysis of posts from Starbucks' Facebook"
    facebook_james.printPosts()
    facebook_james.getLexicalDiversity()
    
    print("\nStarbucks.com Economic Platform: 'Q2 Fiscal 2018 Results'")
    website_summary.get_summary("https://investor.starbucks.com/press-releases/financial-releases/press-release-details/2018/Starbucks-Reports-Record-Q2-Fiscal-2018-Results/default.aspx")
    print("\nStarbucks.com: 'about us: company information'")
    website_summary.get_summary("https://starbucks.com/about-us/company-information")
    print("\nStarbucks Blog Article: 'Equal Pay for Equal Work'")
    website_summary.get_summary("https://starbuckschannel.com/starbucks-announces-pay-equity-for-us-partners-sets-global-goal/")
    website_summary.scrape_profile()
    
main()
