import src

#Flow
# get_locationlist-->try_locationlist-->get_profiledetails

locations = src.get_locationlist('https://www.realtor.com/realestateagents/')
src.try_locationlist(locations)


#src.get_profiledetails('realestateagents/56c5959c7e54f70100225b53')
