import src

#Flow
# get_locationlist-->try_locationlist-->get_agentids-->get_profiledetails
#
locations = src.get_locationlist('https://www.realtor.com/realestateagents/')
src.try_locationlist(locations) if locations else None

