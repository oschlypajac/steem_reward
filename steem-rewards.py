from steem import Steem
from steem.post import Post
from steem.blog import Blog
from coinmarketcap import Market
import datetime

shell = True # Change this to False and input the username bellow (or in your code up here) if you want to not run this in shell.
acc_name = ""
payout_type = True # True for 50/50, False for all SP.

if shell:
	acc_name = input("Your ACC name: @")
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
while x < len(all_posts)-1: # Storing all posts that are less than a week old in a list, with an accuracy of 1 minute.
	post = Post(str(all_posts[x]))
	if post.time_elapsed() < datetime.timedelta(minutes=10080):
		acc_posts.append(all_posts[x])
	x+= 1

x = 0
while x < len(acc_posts)-1: # Collecting rewards for each post and storing them in the "total" variable.
	post = Post(acc_posts[x])
	reward = str(post.reward)
	reward = float(reward.replace("SBD", ""))
	total += reward
	post_dict[acc_posts[x]] = post.reward # Storing all of the posts with their rewards in a dictionary. This is not used in this program, but might be useful to you.
	x+= 1