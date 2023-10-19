from modules.etl import vtypes
from modules.etl import transforms
from modules.etl.config import (
	redcapTransformConfig,
	sexGenderTransformConfig,
	raceEthnicityTransformConfig,
	phenotypeTransformConfig,
	studyWaypointsTransformConfig,
	mixedTransformTestConfig
)

if __name__ == "__main__":

	extract = transforms.REDCapTransform(
		config = redcapTransformConfig
	).merged

	extract.to_csv("merged-transform.tsv", sep = "\t")

	cacheTransforms = [
		sexGenderTransformConfig,
		raceEthnicityTransformConfig,
		phenotypeTransformConfig,
		studyWaypointsTransformConfig,
		mixedTransformTestConfig
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
