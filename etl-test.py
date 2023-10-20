import os, dotenv

from modules.etl import vtypes
from modules.etl import transforms
from modules.etl.config import (
	redcapTransformConfig,
	sexGenderTransformConfig,
	raceEthnicityTransformConfig,
	phenotypeTransformConfig,
	studyWaypointsTransformConfig
)

dotenv.load_dotenv()
REDCAP_API_TOKEN = os.environ["REDCAP_API_TOKEN"]
REDCAP_API_URL = os.environ["REDCAP_API_URL"]

if __name__ == "__main__":

	redcapTransformConfig |= {
		"redcap_api_url": REDCAP_API_URL,
		"redcap_api_key": REDCAP_API_TOKEN,
	}

	extract = transforms.REDCapTransform(
		config = redcapTransformConfig
	).merged

	extract.to_csv("merged-transform.tsv", sep = "\t")

	cacheTransforms = [
		sexGenderTransformConfig,
		raceEthnicityTransformConfig,
		phenotypeTransformConfig,
		studyWaypointsTransformConfig
	]

	# Print
	for module_method, config in cacheTransforms:
		transformer = getattr(transforms.ModuleTransform(config), module_method)(extract)
		if type(transformer.transformed) == list:
			for record in transformer.transformed:
				print(record)
			print("\n")
		if type(transformer.transformed) == dict:
			for key, transform in transformer.transformed.items():
				print(key)
				for record in transform:
					print(record)
else:
		pass
