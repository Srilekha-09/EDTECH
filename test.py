# # Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client


# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# account_sid = 'AC483282f4bea90c5993e20076bf7f6e55'
# auth_token = '64513d72f378add3b78a408a1124572d'
# client = Client(account_sid, auth_token)

# message = client.messages \
#     .create(
#          body='Hello there!',
#          media_url=['https://www.youtube.com/watch?v=JzPfMbG1vrE'],
#          from_='whatsapp:+14155238886',
#          to='whatsapp:+916361276796'
#      )

# print(message.sid)
# jobs = [
#     {
#         'job_name': 'MLOps Engineer',
#   'company_name': 'Confidential Company Name'
#   , 'link': 'https://www.monsterindia.com/job/mlops-engineer-bengaluru-bangalore-6779138?utm_campaign=google_jobs_apply&utm_source=google_jobs_apply&utm_medium=organic',
#   'location': 'Bengaluru, Karnataka'
#     }
# ]

# print(jobs[0]['job_name'])
