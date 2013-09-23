# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for Calendar API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

"""

import argparse
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/218746604801/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))


def main(argv):
  # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Calendar API.
  service = discovery.build('calendar', 'v3', http=http)

  events = service.events().list(calendarId='noterrain@gmail.com').execute()
  # service.events().insert(calendarId='noterrain@gmail.com', body="{u'status': u'confirmed', u'kind': u'calendar#event', u'end': {u'dateTime': u'2013-09-22T17:30:00-04:00'}, u'description': u'This is robtime event', u'created': u'2013-09-23T00:05:23.000Z', u'iCalUID': u'tjd87p4ebs0f8fe0bviv5l7jto@google.com', u'reminders': {u'useDefault': True}, u'htmlLink': u'https://www.google.com/calendar/event?eid=dGpkODdwNGViczBmOGZlMGJ2aXY1bDdqdG8gbm90ZXJyYWluQG0', u'sequence': 0, u'updated': u'2013-09-23T00:05:23.527Z', u'summary': u'Appropriating Interaction Technologies', u'start': {u'dateTime': u'2013-09-22T18:00:00-09:00'}, u'etag': u'"B0R-JqZ1uFKvtifdS4AVDz7BCB4/MTM3OTg5NDcyMzUyNzAwMA"', u'organizer': {u'self': True, u'displayName': u'Tianyu WU', u'email': u'noterrain@gmail.com'}, u'creator': {u'self': True, u'displayName': u'Tianyu WU', u'email': u'noterrain@gmail.com'}, u'id': u'tjd87p4ebs0f8fe0bviv5l7jto'}])",sendNotifications=None, maxAttendees=None)
  print events['items'][0]['end']

  try:
    print "Success! Now add code here."

  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")


# For more information on the Calendar API you can visit:
#
#   https://developers.google.com/google-apps/calendar/firstapp
#
# For more information on the Calendar API Python library surface you
# can visit:
#
#   https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/
#
# For information on the Python Client Library visit:
#
#   https://developers.google.com/api-client-library/python/start/get_started
if __name__ == '__main__':
  main(sys.argv)



