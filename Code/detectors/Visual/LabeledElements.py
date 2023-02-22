import xml.etree.ElementTree as ET
def checkLabeled(xml_path):
# Load the XML file
	if ".DS_S" not in xml_path:
		tree = ET.parse(xml_path)
		root = tree.getroot()

		violations = 0
		nonViolations = 0
		total = 0
		for elem in root.iter():
			elements = elem.items()
			
			if len(elements) > 1:
				if elements[8][0] == 'clickable' and elements[8][1] =='true':
					total += 1
					if len(elements[5][1].strip('\n')) < 2:
						violations += 1
					else:
						nonViolations += 1
					
		return([violations, total, xml_path])