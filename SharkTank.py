import requests, re

# HTTP GET request to fetch the content
r = requests.get('https://gist.githubusercontent.com/murtuzakz/4bd887712703ff14c9b0f7c18229b332/raw/d0dd1c59016e2488dcbe0c8e710a1c5df9c3672e/season7.json')

# Decode JSON response
json_content = r.json()

# Dictnary to maintain the parsed data
parsed_data = {}

# Loop through every episode
for ep_key, episode in json_content.items():

	# Loop through every record in an episode
	for record in episode:
		
		# Skip if no investor has been mentioned
		if not len(record['investors']):
			continue
			
		# Getting the list of all investors
		investors = list(filter(None, re.split('^[\s]+|[\s]*,[\s]*|[\s]*and[\s]*|[\s]+$', record["investors"])))
		
		# Add the company name to the investor's corresponding list
		for investor in investors:
			companies = [record["company"]["title"]]
			if investor in parsed_data and len(parsed_data[investor]):
				# Append with existing companies
				companies.extend(parsed_data[investor])
			parsed_data.update({investor: companies})
		
# Sort investors - maximum number of investments
sorted_investors = sorted(parsed_data, key=lambda k: len(parsed_data[k]), reverse=True)

for investor in sorted_investors:
	print('\r\n', investor, ':', parsed_data[investor])