# bot.py
import random
import discord
import praw
import timeago
import configparser

from discord.ext import commands
from datetime import datetime
from discord.ext import tasks
from discord.ext.tasks import loop

configpath = 'config.ini'
config = configparser.ConfigParser()
config.read(configpath)

BOT_LIMIT=20 #max number of comments during a flush

TOKEN = config.get('DEFAULT','DISCORD_TOKEN')
GUILD = config.get('DEFAULT','DISCORD_GUILD')
DISCORD_SECRET = config.get('DEFAULT','DISCORD_SECRET')
DISCORD_ID = config.get('DEFAULT','DISCORD_ID')

bot = commands.Bot(command_prefix='~')

bot.USERNAME = config.get('DEFAULT','REDDIT_USERNAME')
bot.PASSWORD = config.get('DEFAULT','REDDIT_PASSWORD')
bot.USERAGENT = config.get('DEFAULT','REDDIT_USERAGENT')
bot.CLIENT_ID = config.get('DEFAULT','REDDIT_CLIENT_ID')
bot.CLIENT_SECRET = config.get('DEFAULT','REDDIT_CLIENT_SECRET')

bot.TIME = config.get('VAR','TIME')
bot.CURRTIME= int(datetime.now().timestamp())

bot.SUB_NAME=config.get('VAR','sub_name')

def ex(e):
	print(e)

def login():
	bot.reddit = praw.Reddit(client_id=bot.CLIENT_ID, client_secret=bot.CLIENT_SECRET, password=bot.PASSWORD, 
	user_agent=bot.USERAGENT, username=bot.USERNAME)
	bot.sub = bot.reddit.subreddit(bot.SUB_NAME)

def flatten(responses):
	return ''.join(y+"\n" for y in responses)

def rem_reddit_prefix(s):
	if(s[0:3] in {'t1_','t2_','t3_','t4_','t5_','t6_'}):
		return s[3:]
	return s

def embedify(s):
	emb = discord.Embed(description=s)
	return emb

async def paste_comment(x,ctx):
	print(str(datetime.now())+" - Printing comment : "+x.id)
	if not(str(x.author) == 'None'):
		fullurl = "https://www.reddit.com//comments/"+rem_reddit_prefix(x.link_id)+"//"+x.id+"?context=1"
		d = datetime.fromtimestamp(int(x.created_utc))
		dnow = datetime.fromtimestamp(bot.CURRTIME)
		timer = timeago.format(d,dnow) + d.strftime(" (%d/%m/%y %H:%M:%S IST)")
		responses = ["/u/"+x.author.name,timer,fullurl,"> "+x.body.replace("\n","\n> ")]
		emb = discord.Embed(title="New comment from /r/"+x.subreddit.display_name,color=0xff0000,description=flatten(responses))
		await ctx.send(embed=emb)

async def join_msg(ctx):
	join_quotes = [
		'I have been reborn...',
		'Hear me and rejoice...',
		"Friends, Romans and Times New...",
		"is just the beginning The end is...",
		"Welcome. You must be wondering why I've gathered you here..."
	]
	response = random.choice(join_quotes)
	await ctx.send(embed = embedify(response))	


@bot.event
async def on_ready():
	for guild in bot.guilds:
		if guild.name == GUILD:
			break
	print(f'{bot.user} is connected to the following guild:')
	print(f'{guild.name}(id: {guild.id})\n')
	members = '\n - '.join(['"'+member.name+ '" ("'+member.display_name+'")' for member in guild.members])
	print(f'Guild Members:\n - {members}')
	print("Bot started...")

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
	print("Command call : 99")
	brooklyn_99_quotes = [
		'I\'m the human form of the 💯 emoji.',
		'Bingpot!',
		(
			'Cool. Cool cool cool cool cool cool cool, '
			'no doubt no doubt no doubt no doubt.'
		),
	]
	response = random.choice(brooklyn_99_quotes)
	await ctx.send(embed=embedify(response))

@bot.command(name='flush', help='Change time in file')
@commands.has_role('admin')
async def flush(ctx):
	print("Command call : flush")
	bot.TIME=bot.CURRTIME
	print("Setting TIME variable as :"+str(bot.TIME))
	config.set('VAR', 'TIME', str(bot.TIME))
	with open(configpath, 'w') as configfile:
	    config.write(configfile)

@bot.command(name='die', help='Kill bot (Admin)')
@commands.has_role('admin')
async def kill(ctx):
	death_quotes = [
		'...Goodbye, cruel world',
		'...Initiate Order 66',
		"...It's treason then",
		'...Oh no, not again',
		'...Okay byeeee',
		"...Why hast thou forsaken me, master"
	]
	response = random.choice(death_quotes)
	await ctx.send(embed=(embedify(response)))	
	printer.cancel()
	await bot.close()
	print("...Bot stopped")

@bot.command(name='display', help='Display all config for Reddit (Admin)')
@commands.has_role('admin')
async def config_disp(ctx):
	print("Command call : display")
	responses = ["Reddit account is : /u/"+bot.USERNAME,"Subreddit is : /r/"+bot.SUB_NAME]
	await ctx.send(embed=(embedify(flatten(responses))))

@bot.command(name='sub', help='Change subname for Reddit config (Admin)')
@commands.has_role('admin')
async def config_sub(ctx, new_sub_name):
	print("Command call : sub")
	bot.SUB_NAME=new_sub_name
	response="Subreddit changed successfully to : /r/"+bot.SUB_NAME
	await ctx.send(embed=embedify(response))

@bot.command(name='setting', help='New account settings (Username, Password, Useragent, ClientID, ClientSecret)')
@commands.has_role('admin')
async def config_setting(ctx, new_uname, new_pw, new_useragent, new_clientid, new_clientsecret):
	print("Command call : setting")
	bot.USERNAME = new_uname
	bot.PASSWORD = new_pw
	bot.USERAGENT = new_useragent
	bot.CLIENT_ID = new_clientid
	bot.CLIENT_SECRET = new_clientsecret
	responses=["New username for Reddit : /u/"+bot.USERNAME, "New password for Reddit : "+bot.PASSWORD, 
	"New Useragent name : "+bot.USERAGENT, "New Client Id : "+bot.CLIENT_ID, "New Client Secret : "+bot.CLIENT_SECRET]
	await ctx.send(embed=embedify(flatten(responses)))

@bot.command(name='setup', help='Try connecting with current config')
async def connect(ctx):
	print("Command call : setup")
	response="Trying to login to :"+bot.SUB_NAME
	await ctx.send(embed=embedify(response))
	try:
		login()
	except Exception as e:
		response="Error found :"+str(e)
		await ctx.send(embed=embedify(response))
	print("Connecting to /r/"+bot.SUB_NAME+": "+str(bot.reddit))

@bot.command(name='stop', help='Stop reading from sub')
async def cancel_run(ctx):
	print("Command call : stop")
	response="Stopping run..."
	await ctx.send(embed=embedify(response))
	printer.cancel()

@bot.command(name='start', help='Start reading from sub')
async def scheduled_run(ctx):
	try:
		print("Running module at :"+str(bot.CURRTIME))
		response="Starting run..."
		await ctx.send(embed=embedify(response))
		printer.start(ctx)
	except Exception as e:
		print("Exception :"+str(e))


@loop(seconds=60)
async def printer(ctx):
	try:
		flag=False
		t=0
		bot.CURRTIME=int(datetime.now().timestamp())
		revv = []
		for x in bot.sub.comments(limit=BOT_LIMIT):
			revv = revv + [x]
		revv.reverse()
		for x in revv:	
			print("Testing comment :"+x.id)
			if(t==0):
				t = int(x.created_utc)
			if(int(x.created_utc)<=int(bot.TIME)):
				flag=True
			else:
				await paste_comment(x,ctx)
		if(flag==False):
			d = datetime.fromtimestamp(t)
			dnow = datetime.fromtimestamp(bot.CURRTIME)
			timer = timeago.format(d,dnow)
			response="Skipping comments before "+timer
			await ctx.send(embed=embedify(response))
		await flush(ctx)
	except Exception as e:
		print("Exception :"+str(e))

# Running Code
login()
bot.run(TOKEN)



# Bot cannot reply to message exception
# If trying to talk in not-Permitted channels
# Exception handler (PM?)
# Call join-command() and ~continue at start on two default guilds
# Private settings for username-pw combos etc
#Multiple subs to track
#Soni backdoor
#Sir Lancebot
#UTC timings
#Heroku
#multiple sub watcher
#multiple instances of bot in same server
#Exception - Subreddit not found