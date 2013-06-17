#!/usr/bin/python
rel = True #For easy debugging set to False
if(rel):
   import Skype4Py #Import the Skype4Py library to connect to Skype.
import re #Import the regular expression's library to make easy work of finding die roll requests.
import time
import random
import string
#Connect to Skype using the x11, because the other one is glitchy.
if(rel):
   skype = Skype4Py.Skype(Transport="x11")
#My old regex.
#d20Match = re.compile(u'(((\d+)[dD](\d+))([kl](\d+))?([-+]?\d+)?)')
   
#New awesome regex. Courtasy of ProfessorRude
"""
this one finds all individual rolls within a pile of rubbish, it's complicated, so:

--- [1-9]\d*[dD][1-9]\d* --- 				this part looks for X Y-sided dice in the format XdY or XDY, obviously, number of sides and dice is nonzero
--- [1-9]\d*[dD][1-9]\d*([kK][1-9]\d)* ---
(\d*[dD]\d*)([kK]\d)*
      (\d*[dD]\d*)([kK]\d)* ---Edited to allow for keep rolls
--- (?:[\+-](?:(?:[1-9]\d*[dD][1-9]\d*)|(?:\d+)))* ---	this part looks for zero or more repetitions of either another die or a modifier, while not memorising anything

    modifier look like +Z or -Z and can be zero, even if that's pointless, another die looks same as above


(?:[\+-](?:(?:(\d*[dD]\d*)([kK]\d)*)|(?:\d+)))* 
"""
dieRoll = "[1-9]\d*[dD][1-9]\d*(?:[kK]\d*)?(?:[rR]\d*)?" #Yay for keep rolls.
repRoll = "(?:[\+-](?:(?:" + dieRoll + ")|(?:\d+)))*"
findrolls = re.compile("[\s]" + dieRoll + repRoll)

"""
this one finds individual dice and their modifiers in what is found by the above, as well as how to add dice if there is more than one to roll

--- ([1-9]\d*)[dD]([1-9]\d*) ---			this part finds the number of dice and their sides, memorising both separately

--- ((?:[\+-]\d+(?![dD]))*) ---				this part finds the modifier - if there is one - while making sure that it's not in fact the start of another die, it memorises the complete modifier string, we'll parse it later
							it accepts stacked modifiers (like 1d20+10+5) in case the player is unable to do basic arithmetic

--- ([\+-])? ---					this part checks if another die follows, and if so, memorises the sign so we know to add or subtract it

"""

rollers = []
rolltimes = []
dieRoll2 = "([1-9]\d*)[dD]([1-9]\d*)(?:[kK](\d*))?(?:[rR](\d*))?" #Keep rolls everywhere.
#Now with rerolls
finddie = re.compile (dieRoll2 + "((?:[\+-]\d+(?![dD]))*)([\+-])?")
def roll_die(sides): #ProfessorRude
   return random.randint(1, sides)
      
def parse_roll(roll): #ProfessorRude
   global finddie
   returnString = "\"" + roll.strip() + "\" "
   dice = finddie.finditer(roll)
   total = 0
   sign = '+'
   for match in dice:
      returnString += "["
      dice_total = 0
      # roll all the dice, enclose in parentheses
      n_dice = int(match.group(1))
      if(n_dice > 2000):
         returnString +=" Too much rolling broseph]"
         return returnString
      if(len(match.group(2)) > 7):
         returnString +=" Too much rolling broseph]"
         return returnString
      rolled = []; #Edits for keep rolls.
      n_sides = int(match.group(2))
      for n in range (0, n_dice):
         res = 0
         if(match.group(4) and int(match.group(4)) < n_sides):
            print("reroll")
            res = roll_die(n_sides - int(match.group(4))) + int(match.group(4))
         else:
            res = roll_die(n_sides)

               
         rolled.append(res)
         
      
         
         
      if(match.group(3)): #If this is a keep roll
         rolled = sorted(rolled) #Sort the results
         rolled.reverse() #Reverse it
      toKeep = int(match.group(3) or 0)
      
      if(toKeep > n_dice):
         toKeep = n_dice
      for i in range(len(rolled)):
         returnString += str(rolled[i]) #Add the number to the return string.
         #If there isn't a keep roll, add the number.
         #If there IS a keep roll check the bounds of it.
         if((not toKeep) or (i < toKeep or toKeep >= n_dice)):
            dice_total += rolled[i] #Add the total
         elif(match.group(3)):
            returnString += "-" #If the keep roll says to chuck the number, add a - after it
            
         if i != n_dice-1:
            returnString += ","
     
      returnString += "]"
      # add all the modifiers for this series, if any, not enclosed
      if match.group(5):
         returnString += match.group(5)
         modifiers = re.findall("[\+-]\d+", match.group(5))
         for modifier in modifiers:
            dice_total += int(modifier) # i assume here that nobody will write something like 1d20+020 and thereby get a modifier in base-8
      if sign == '-':
         total -= dice_total
      else:
         total += dice_total
      
      if match.group(6):
	 # set the sign for the next die series, print it enclosed in braces to separate die series
         returnString += "" + match.group(6) + ""
         sign = match.group(6)
      
   returnString += " = " + str(total)
   print returnString[:64]
   return returnString

#If the client is not already running start it.
if(rel):
   if not skype.Client.IsRunning:
      skype.Client.Start()

#This is what Skype will ask the user to allow access to Skype.
if(rel):
   skype.FriendlyName = 'DiceBot'

#This is what it says when you ask it for help.
spew = "Commands:\n#1d#2 rolls a #2 sided die #1 times.\n"
spew += "#1 is a numerical placeholder (don't type the # symbol pls)\n"
spew += "#1d#2k#3 rolls a #2 sided die #1 times and keeps the #3 highest rolls\n"
spew += "#1d#2k#3r#4 rolls a #2 sided die #1 times and keeps the #3 highest rolls, but rerolls if the roll is #4 or less.\n"
spew += "You can type +/- after a roll to add or subtract from it.\n"
spew += "eg. 1d12+5 adds five to the roll.\n"
spew += "Limit of 2000 rolls at once.\n"
spew += "You must wait a second between rolls (to prevent le spam).\n"
spew += "Comments can be sent to Skype user \"mustyoshi\""

#When somebody friend requests the bot, auto accept it. And print to the console that we added it.
def reqd(user):
   user.SetBuddyStatusPendingAuthorization(Skype4Py.budFriend)
   print "Added:" + user.Handle

class Debug():
   cmsReceived = 1
if(not rel):
   Skype4Py = Debug()
msg = Debug()
msg.Body = "4d6r1"
msg.FromDisplayName = "test"

#This is where the magic happens.
def msgd(msg, status):
   #print status #Debug stuff, ya know.
   #If the status is that we received it, then we can operate on it.
   if(status == Skype4Py.cmsReceived):
      
      #Mark it as seen.
      if(rel):
         msg.MarkAsSeen()

      #Check for matches of the regex.
      plsstop = False
      #try:
            #ind = rollers.index(msg.FromDisplayName)
            #if(rolltimes[ind] > time.time() -1):
                  #plsstop = True
            #else:
                  #rolltimes[ind] = time.time()
            
      #except:
            #rollers.append(msg.FromDisplayName)
            #rolltimes.append(0)

      if(plsstop):
            return
      returnString = msg.FromDisplayName + " rolled:"
      rolls = findrolls.findall(" " + msg.Body)
      #hand them off one by one
      for roll in rolls:
         returnString+= "\n"+ parse_roll(roll)
      if(rel and rolls):
         msg.Chat.SendMessage(returnString)

      elif(rolls): #That feel when forget to check if anything was even rolled
         print returnString
   else:
      #This is a catch for if I am watching the people RP and I cause the wrong event(cmsRead) to be thrown.
      #if(status == Skype4Py.cmsRead and ((time.time() - msg.Timestamp) < 60)):
         #print "wut"
         #msgd(msg,Skype4Py.cmsReceived)
      if(msg.Body == "help"):
         msg.Chat.SendMessage(spew);


if(not rel):
   print "wat"
   msgd(msg,Skype4Py.cmsReceived)
skype.OnMessageStatus = msgd
skype.OnUserAuthorizationRequestReceived = reqd
print "Attaching"
try:
   skype.Attach(30,False)
except:
   pass
print "Attached"
while(True):
   if not skype.Client.IsRunning:
      print "Not running, attempting to start"
      skype.Client.Start()
   if skype.AttachmentStatus != Skype4Py.apiAttachSuccess:
      try:
         print "Attempting to attach"
         skype.Attach(30,False)
      except:
         pass
   time.sleep(30)
print "quitting"
