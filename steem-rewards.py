from steem import Steem
from steem.post import Post
from steem.blog import Blog
from coinmarketcap import Market
import datetime

shell = True # Change this to False and input the username bellow (or in your code up here) if you want to not run this in shell.
acc_name = ""
payout_type = True # True for 50/50, False for all SP.

if shell:
	acc_name = input("Your steem account name: @")
	print('Please wait while we connect to the steem blockchain.')

blog = Blog(acc_name).all()
all_posts = []
acc_posts = []
post_dict = {}
total = 0

for a in blog: # Storing all posts in a list as links.
	astr = str(a).split("-")[1:]
	astr = "-".join(astr)
	astr = astr.replace(">", "")
	astr = "https://steemit.com/" + astr
	all_posts.append(astr)

x = 0
while x < len(all_posts): # Storing all posts that are less than a week old in a list, with an accuracy of 1 minute.
	post = Post(str(all_posts[x]))
	if post.time_elapsed() < datetime.timedelta(days=7):
		acc_posts.append(all_posts[x])
	x+= 1

x = 0
while x < len(acc_posts): # Collecting rewards for each post and storing them in the "total" variable.
	post = Post(acc_posts[x])
	reward = str(post.reward)
	reward = float(reward.replace("SBD", ""))
	total += reward
	post_dict[acc_posts[x]] = post.reward # Storing all of the posts with their rewards in a dictionary. This is not used in this program, but might be useful to you.
	x+= 1

cmc = Market() # Coinmarketcap API call.
# Checking the live values of Steem and SBD.
ste_usd = cmc.ticker("steem", limit="3", convert="USD")
ste_usd = ste_usd[0].get("price_usd", "none")
sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")
sbd_usd = sbd_usd[0].get("price_usd", "none")
total = float(total)

# A function for calculating and displaying the potential rewards in USD if you chose 50/50 in SBD and SP.
def outcome5050(total,sbd,ste):
	total = float(total) * 0.8 # Currator cut, anywhere between 0.85 and 0.75.
	totalsbd = str(total * 0.5 * float(sbd))[:6]
	totalsp = total * 0.5 * float(ste)
	totalsp = str(totalsp * 1/float(ste))[:6] # SBD is always worth 1$ in the steem blockchain, so price of SBD to price of STE is always 1/STE.
	payout = str(float(totalsbd) + float(totalsp))[:6]
	print("You will receive " + totalsbd + " USD worth of SBD and " + totalsp + " USD worth of SP for a total of " + payout + " USD." ) # The print if you just want to run this from your shell.

	outc = {
	"SP" : totalsp,
	"SBD" : totalsbd, 
	"Total" : payout}
	return outc # The return if you want to use this as a base for your program.

def outcomeSP(total,ste):
	total = float(total * 0.8)
	totalsp = total * float(ste)
	totalsp = str(totalsp * 1/float(ste))[:6]
	print("You will receive " + totalsp + " USD worth of SP.")

	outc = {
	"SP" : totalsp
	}
	return outc

# Calling the functions based on your choice and ending the program.
if payout_type:
	outcome5050(total,sbd_usd,ste_usd) 
else:
	outcomeSP(total,ste_usd)