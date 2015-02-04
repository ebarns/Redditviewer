from BeautifulSoup import BeautifulSoup as Soup
import mechanize
import urllib
import re
def main():
	#welcome to the progam
        print("WELCOME TO THE REDDIT VIEWER \n")
	#ask for what subreddit to access and retrieve the posts
        contents = get_posts()
	#begin listener loop, waiting for commands
        while(True):
		#ask what user would like to do
                post_num = input("What would you like to do?  ")
                if(post_num == "EXIT" or post_num=="exit"):
			print("\n****THANKS FOR BROWSING****")
                        break
                elif(post_num == "SWITCH" or post_num == "switch"):
                        #new_sub = input("Enter name of subreddit you want to visit")
                       	contents =  get_posts()
                        #call upon listing process

                else:
			if(post_num > len(contents)):
				print("Please give a number within the post range")
			else:
				#user is giving us an index of a post
				#retrieve the comments link of the index request
                        	comments = contents[post_num-1].find('li',{"class":"first"})
                        	new_link = comments.a['href']
				#print out the title and top comment of the requested post
                        	title ="\nTITLE: "+contents[post_num-1].a.string
                        	title = title.replace('&quot;','"')
				print(title)
				print(find_top(new_link))

def get_posts():
	#ask for subreddit11
	sub = input("What subreddit would you like to see? ")
	link = "http://www.reddit.com/r/"+sub
#create soup object
	response = br.open(link).read()
#	url = urllib.urlopen(link)
#	html = url.read()
	soup = Soup(response)

#pull all of the posts from first page
	table = soup.find('div',{'id':'siteTable'})
	contents = table.findAll('div',{'class': 'entry unvoted'})
#loop through all of the posts
#print their title and an index by which the user can further access the post
	for k,post in enumerate(contents):
		print ("["+str(k+1)+"]  " + post.a.string + "\n")

#ask for post to view or other command
	print("\nBy typing the index number of the post you can obtain further information")
	print("Type SWITCH change subreddits")
	print("Type EXIT to stop browsing reddit")
	return contents
		
#follow post

def find_top(comments_link):
#	print(comments_link)
	#give comments link and read the html
	response = br.open(comments_link)
	html = response.read()
#	html = urllib.urlopen(comments_link).read()
	#soup the html
	soup = Soup(html)
	#ps will store all of the paragraphs that BS finds from forms
	ps = []
	#usertext is the class name for forms constaining user posts
	try:
		op_content = soup.find('div',{"id":"siteTable"})
		post = op_content.find('div',{"class":"md"})
		post_descrip = post.p.string
		print("Post Description: " + str(post_descrip))
	except:
		print("Post Description: None Available \n")
	commentarea = soup.find('div',{"class":"commentarea"})
	top_text = commentarea.findAll('form',{"class":"usertext"})
	#grab all paragraphs per post and place them in ps
	#bound should be placed on loop to speed up process
	for m, text in enumerate(top_text):
		if(m > 10):
			break
        	usr_comment = text.find('p')
        	ps.append(usr_comment)
	#loop through <p>'s
	#after 5 paragraphs break, top comment no there
	#use regex to check if the para.string is sentence not link
	#if it is link or other content, just pass we don't want that
	for k, para in enumerate(ps):
	       	if(k>5):
                	print("breaking")
                	break
        	try:
				#print(para)
                	re.compile("(\w+.*\s*)+").findall(para.string)
			return("Top comment:"+str(para.string)+"\n")
        	except:
#			print("passing")
                	pass
#initialize mechanize browser
#this will give me user status and my requests won't be blocked
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent','Firefox')]
main()
