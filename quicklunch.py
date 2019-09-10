"""QuickLuncheon."""
import os
import json
import random
import time
import maya.cmds as cmds
# to grab Human-readable file form rnkRig.
from rigging.core import utils

"""
QuickLuncheon is for Users that needs to to decide on a Quick Lunch
decisions. The concept of this app will randomize the closest
restaurant near you or just give you a full list of restaurants.
The App Must be SUPER simple to use so Users can just understand how to
use it without instructions.

@TODOS: Make "Add New Restaurant"
@TODOS: when you select the restaurant in these list make window pop up
    	with menu and phone number
"""


class QuickLunch(object):

	"""doc-string for QuickLunch."""

	def __init__(self):
    	"""All the require path."""
    	paths = '/corp/projects/eng/tsong/workspace/rnkRigDev/Personal/tsong'
    	self.restaurants_path = '%s/QuickLunch/Restaurants' % paths
    	self.message_path = '%s/QuickLunch/message.json' % paths
    	self.history_path = '%s/QuickLunch/History/dataHistory.json' % paths

	def final_results(self):
    	"""Combine random message and restaurant."""
    	# self in to single strings & easy to read
    	theAnswer = []
    	# message = self._message_of_the_day()
    	restaurant = self._randomized_restaurant()
    	# End self
    	# theAnswer.append(message)
    	theAnswer.append(restaurant)
    	# Updating new dict @ _update_data_history
    	self._update_data_history(restaurant)
    	# End Updating
    	return theAnswer

	def restaurant_list(self):
    	"""A list of all restaurants in restaurants file."""
    	# all the file in ../../QuickLunch/Restaurants add in name for each
    	# file without the .json
    	restaurants = []
    	# removeExFiles = ['.svn'] # Just future idea.
    	restaurants_path = os.listdir(self.restaurants_path)
    	restaurants_path.remove('.svn')
    	# restaurants_path.remove('temp.json')
    	# os.listdir  will look in the paths and read whats in the directory
    	for restaurantsList in restaurants_path:
        	# the path to all the restaurant Data
        	restaurants_path = os.path.join(self.restaurants_path,
                                        	restaurantsList)
        	# below this code utils.parse_json_with_comments is a
        	# Parse .json files that have C-style comments (// /**/).
        	dataRestaurants = utils.parse_json_with_comments(restaurants_path)
        	dataRestaurants = json.load(open(restaurants_path))
        	json.dump(dataRestaurants, open(restaurants_path, 'w'),
                  	indent=4)
        	# storing the
        	restaurants.append(dataRestaurants['name'])
        	# print restaurants
    	return restaurants

	def _message_of_the_day(self):
    	"""A list of message that becomes random."""
    	# self in to single strings & easy to read
    	message_path = os.path.join(self.message_path)
    	# End self

    	# below this code utils.parse_json_with_comments is a
    	# Parse .json files that have C-style comments (// /**/).
    	dataMessage = utils.parse_json_with_comments(message_path)
    	dataMessage = json.load(open(message_path))
    	json.dump(dataMessage, open(message_path, 'w'), indent=4)

    	message = dataMessage['message']
    	FinalMessageResult = (message[random.randint(0, len(message)-1)])
    	return FinalMessageResult

	def _randomized_restaurant(self):
    	"""randomize restaurants dont come up twice."""
    	# self in to single string
    	restaurants = self.restaurant_list()
    	thePreviousHis = self._initializing_randomized_restaurant()
    	# End self

    	# randomizing restaurant restaurant_list
    	ResturantResult = (restaurants[random.randint(0,
                       	len(restaurants)-1)])
    	# randomizing restaurant restaurant_list again, so its not
    	# getting the same result from previous history list
    	while ResturantResult in thePreviousHis:
        	ResturantResult = (restaurants[random.randint(0,
                           	len(restaurants)-1)])
    	# End of randomizing
    	return ResturantResult

	def _initializing_randomized_restaurant(self):
    	"""randomize non-existing names from last 4 dictionaries."""
    	# self in to single string
    	theDataHistory = self._get_data_history()
    	# End self

    	# FINDING the last 4 dictionaries in dataHistory.json
    	dictList = theDataHistory['RestaurantsHistory'][-4:]

    	# CREATING new list under newlist for the last 4 dictionaries
    	newlist = []
    	for allitem in dictList:
        	newlist.append(allitem['restaurant'])

    	return newlist

	def _get_data_history(self):
    	""" copy all the previous history."""
    	# remider that json.load() will copy the .json file
    	theHistory = open(self.history_path)
    	holdHistory = json.load(theHistory)
    	theHistory.close()

    	return holdHistory

	def _update_data_history(self, restaurant):
    	"""To Store new entry with the old History."""
    	# choice_of_the_day will be created as dictionary
    	choice_of_the_day = dict()
    	# writes the Key('date') as the time
    	choice_of_the_day['date'] = time.time()
    	# writes the Value('restaurant') as the FinalResturantResult
    	choice_of_the_day['restaurant'] = restaurant
    	# appending new history information
    	holdHistory = self._get_data_history()
    	"""To remove 1 after maxCapDic(12) entries."""
    	# theHisDic holds only RestaurantsHistory
    	theHisDic = holdHistory['RestaurantsHistory']
    	# counting the how many dictionaries in theHisDic
    	numOfDic = len(theHisDic)
    	# the maximum of dataHistory.json should hold.
    	maxCapDic = 12
    	# if dataHistory.json has more than 16 dic then
    	# remove the first element
    	if numOfDic >= maxCapDic:
        	theHisDic.pop(0)
        	# if not just pass it.
    	else:
        	pass
    	# choice_of_the_day = holdHistory.update(choice_of_the_day)
    	holdHistory['RestaurantsHistory'].append(choice_of_the_day)
    	# storing in Old + New history information
    	with open(self.history_path, mode='w') as inputHistory:
        	json.dump(holdHistory, inputHistory, sort_keys=True, indent=4)
# ======================================================================
def AddNewRestaurant(self):
	"""Initializing AddNewRestaurant Window."""
	# Define an id string for the window first
	winID = 'AddNewRestaurant'
	# Test to make sure that the UI isn't already active
	if cmds.window(winID, exists=True):
    	cmds.deleteUI(winID)
	# Now create a fresh UI window
	ANR = cmds.window(winID, iconName='QL')
	# Add a Layout - a columnLayout stacks controls vertically
	cmds.rowColumnLayout(numberOfColumns=2,
                     	columnAttach=(1, 'both', 0),
                     	columnWidth=[(1, 80), (2, 150)])
	# creating catagories
	cmds.text(label='Name:', align='left')
	name = cmds.textField()
	cmds.text(label='Type:', align='left')
	Type = cmds.textField()
	cmds.text(label='Phone Number:', align='left')
	phoneNumber = cmds.textField()
	cmds.text(label='MeatDish:', align='left')
	MeatDish = cmds.textField()
	cmds.text(label='VegeDish:', align='left')
	VegeDish = cmds.textField()

	#	Attach commands to pass focus to the next field if the Enter
	#	key is pressed. Hitting just the Return key will keep focus
	#	in the current field.

	cmds.textField(name, edit=True,
               	enterCommand=('cmds.setFocus(\"' + Type + '\")'))
	cmds.textField(Type, edit=True,
               	enterCommand=('cmds.setFocus(\"' + phoneNumber + '\")'))
	cmds.textField(phoneNumber, edit=True,
               	enterCommand=('cmds.setFocus(\"' + MeatDish + '\")'))
	cmds.textField(MeatDish, edit=True,
               	enterCommand=('cmds.setFocus(\"' + VegeDish + '\")'))
	cmds.textField(VegeDish, edit=True,
               	enterCommand=('cmds.setFocus(\"' + name + '\")'))

	# creating buttons together.
	cmds.rowColumnLayout(numberOfColumns=1,
                     	columnAttach=(1, 'both', 0),
                     	columnWidth=[(1, 100), (2, 150)])
	cmds.setParent('..')
	cmds.rowColumnLayout(numberOfColumns=1)
	cmds.button(label='Create', align='center', w=150, h=20)
	cmds.button(label='Cancel',
            	command=('cmds.deleteUI(\"' + ANR + '\", window=True)'),
            	align='center', w=100, h=20)
	cmds.showWindow(winID)

# ======================================================================
def QuickLunchButton(self):
	"""
	When Quick Lunch Button is pushed.
	same window with NEW random Restaurant Result.
	"""
	# Define an id string for the window first
	winID = 'QuickLuncheon'
	# Test to make sure that the UI isn't already active
	if cmds.window(winID, exists=True):
    	cmds.deleteUI(winID)
	# Now create a fresh UI window
	cmds.window(winID, iconName='QL', widthHeight=(150, 300))
	# Add a Layout - a columnLayout stacks controls vertically
	cmds.columnLayout(rowSpacing=5, columnWidth=170)
	# QUICK LUNCH BUTTON------------------------------------------------
	obj = QuickLunch()
	cmds.button(label='Quick Lunch',
            	command=QuickLunchButton,
            	w=150, h=50)
	# RESULT OF THE DAY-------------------------------------------------
	# getting from QuickLunch class
	theMsg = []
	theMotD = obj._message_of_the_day()
	theMsg.append(theMotD)
	# For message of the day
	cmds.text(label=theMsg[0],
          	w=150)
	# getting from QuickLunch class
	theResults = obj.final_results()
	# For Restaurant of the day
	cmds.textScrollList(numberOfRows=1,
                    	allowMultiSelection=True,
                    	append=theResults,
                    	showIndexedItem=4,
                    	w=150)
	# RESTAURANT LIST---------------------------------------------------
	# getting from QuickLunch class
	cmds.text(label='Restaurant List:',
          	align='center',
          	w=150)
	# Add controls into this Layout
	thelst = obj.restaurant_list()
	numberOfRestaurant = len(thelst)
	cmds.textScrollList(numberOfRows=numberOfRestaurant,
                    	allowMultiSelection=False,
                    	append=thelst,
                    	showIndexedItem=5,
                    	w=150)
	# ------------------------------------------------------------------
	cmds.button(label='Add New Restaurant',
            	command=AddNewRestaurant,
            	align='center', w=150, h=20)
	# Display the window
	cmds.showWindow(winID)

# ======================================================================

"""initializing QuickLunch Window."""

# Define an id string for the window first
winID = 'QuickLuncheon'
# Test to make sure that the UI isn't already active
if cmds.window(winID, exists=True):
	cmds.deleteUI(winID)
# Now create a fresh UI window
cmds.window(winID, iconName='QL', widthHeight=(150, 230))
# Add a Layout - a columnLayout stacks controls vertically
cmds.columnLayout(rowSpacing=5, columnWidth=170)
# QUICK LUNCH BUTTON----------------------------------------------------
cmds.button(label='Quick Lunch',
        	command=QuickLunchButton,
        	w=150, h=50)
# RESULT OF THE DAY-----------------------------------------------------
cmds.text(label="Push ^ Quick Lunch ^ to...",
      	align='center',
      	w=150)
cmds.textScrollList(numberOfRows=1,
                	allowMultiSelection=False,
                	append="Randomize Restaurant",
                	w=150)
# RESTAURANT LIST-------------------------------------------------------
cmds.text(label='Restaurant List:',
      	align='center',
      	w=150)
# Add controls into this Layout
obj = QuickLunch()
thelst = obj.restaurant_list()
numberOfRestaurant = len(thelst)
cmds.textScrollList(numberOfRows=numberOfRestaurant,
                	allowMultiSelection=False,
                	append=thelst,
                	showIndexedItem=5,
                	w=150)
# ----------------------------------------------------------------------
cmds.button(label='Add New Restaurant',
        	command=AddNewRestaurant,
        	align='center', w=150, h=20)
# Display the window
cmds.showWindow(winID)


