
#####################################################
# Title:        grammarnazi5000.py                  #
# Devguy:       idont                               #
# Date:         13-14th of August, 2016             #
#####################################################

# Description:  grammarnazi5000 is a state of the art grammar nazi, it will
# change Slack as we know it today. Not only does it check for basic grammar
# mistakes, but it also calls you out on it (fucking loser!). grammarnazi5000
# was born for a slackbot hackathon for the newbiecorner, organized by our
# lovely lana - please take some credz. Awesome chall!
#
# RTFM (READ THE FUCKING MANUAL!!!) on how to install your new grammar nazi today!


import os
import time
import re
import ConfigParser
from slackclient import SlackClient



# Where the magic Happens - not proud...
def handle_command(command, channel):
    # Default response
    response = 0

    # Debugging - prints a message in a channel
    #print command

    # dodgy af. beautiful, but dirty hacks in this dirty hackathon<3
    if re.match("^I'm grammarnazi5000", command):
        return response
        # This if-statement is very hackable.. Just sayin'

    elif re.match('^[a-z]', command):
        response = "I'm grammarnazi5000, and you gotta lern how2capitalize!"

    elif (re.match(".*(([\,\?\!]{2,})|(\.{4,}))", command)):
        response = "I'm grammarnazi5000. Assshole, please stop exaggerating!"

    elif re.match(".*(([Tt][Hh][Ee][Yy]'[Rr][Ee])|([Tt][Hh][Ee][Ii][Rr]))", command):
        response = "I'm grammarnazi5000. Sure taht 'their' is not mixed "\
            "up with 'they're'?"

    elif (not re.match("^[A-Z]['A-Za-z0-9]* [A-Za-z0-9]+", command)):
        response = "I'm grammarnazi5000. This canot possibly be complete!"

    elif (re.match("^[A-Z0-9 \!\?\.\,\\\\/\{\}\[\]\+\=\-\_]*$" ,command)):
        response = "I'm grammarnazi5000. Dude, relxa!"


    if (response):
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)



# Some weird ass parsing crap - it is responsible for lurking the channel
# Perhaps it even deserves a renaming to something like 'creepyStalker'?
def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                return output['text'].strip(), output['channel']
    return None, None



## HELPER FUNCTION - for config ##
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1



# Config/setup crap
Config = ConfigParser.ConfigParser()
Config.read('config.py')
BOT_ID = ConfigSectionMap("Config")['id']
TOKEN = ConfigSectionMap("Config")['token']
slack_client = SlackClient(TOKEN)



# int main - but in python and more like void than int. #yolo
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 0.2
    if slack_client.rtm_connect():
        print("grammarnazi5000 is correcting your grammar like never before!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. You suck at computers - me, "\
                "the dev have never even experienced this.. Just sayin'..")
