import facebook_james
import starbucks

def main():
    print "Analysis of posts from Starbucks' Facebook"
    facebook_james.printPosts()
    facebook_james.getLexicalDiversity()
    
    print("\nStarbucks.com Economic Platform: 'Q2 Fiscal 2018 Results'")
    starbucks.get_summary("https://investor.starbucks.com/press-releases/financial-releases/press-release-details/2018/Starbucks-Reports-Record-Q2-Fiscal-2018-Results/default.aspx")
    print("\nStarbucks.com: 'about us: company information'")
    starbucks.get_summary("https://starbucks.com/about-us/company-information")
    print("\nStarbucks Blog Article: 'Equal Pay for Equal Work'")
    starbucks.get_summary("https://starbuckschannel.com/starbucks-announces-pay-equity-for-us-partners-sets-global-goal/")
    
main()
