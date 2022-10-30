# Striped XML to Turtle
Are your XML documents [striped](https://www.w3.org/2001/10/stripes/)? If so, they may be convertable to triples/graph form.  
Note that the conversion follows my own made up set of rules since there is no official means of converting "just any XML document to triples" (that I'm aware of).  
  
Developed on Windows 10, Python 3.8.3. 

## Install
1. `python3 -m venv env`
2. `. env/bin/activate` (or `env\Scripts\activate.bat` if Windows)
3. `cd env`
4. `pip install -r requirements.txt` (`pip install -r requirements-dev.txt` if you want to dev but all that really adds is flake8)
5. `python stripedXmlToTurtle.py --help`

## Options
- xmlFile
    - Path to your input XML file
    - The only **required** parameter, everything else is optional
- serializePath
    - Path to where your serialized data should be saved
    - If not provided, the graph will be printed
    - If provided (and assuming the conversion is successful, it's going to print the result of serialization which is something like `[a rdfg:Graph;rdflib:storage [a rdflib:Store;rdfs:label 'Memory']].`)
- outputFormat
    - The output format of the graph. Uses the built in rdflib formats where relevant.
    - "turtle" (default), "xml", "n3", "nt", "pretty-xml", "trig", "json-ld", or "hext"
- collectAttributes
    - If this is set, attributes in the document will be picked up for conversion. Since the attributes do not have a namespace, they will take on the namespace of the tag they were found in, otherwise defaults to the default namespace.
- noIgnoreWhitespace
    - Do not ignore whitespace. Prettified XML documents have whitespace, for example. Not sure why you would want to set this.
- defaultNamespace
    - Set a default prefix and URI to be used
    - Defaults to "ex" and "http://example.org/#"

## Sample Data
`python stripedXmlToTurtle.py input.xml --collectAttributes --serializePath output.ttl`
#### XML Input
```
<gmd:MD_Metadata xmlns:gss="http://www.isotc211.org/2005/gss" xmlns:gts="http://www.isotc211.org/2005/gts" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:functx="http://www.functx.com" xmlns:gmi="http://www.isotc211.org/2005/gmi" xmlns:gmx="http://www.isotc211.org/2005/gmx" xmlns:gsr="http://www.isotc211.org/2005/gsr" xmlns:srv="http://www.isotc211.org/2005/srv" xmlns="http://www.isotc211.org/2005/gmi" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd">
	<gmd:fileIdentifier>
		<gco:CharacterString>myXMLDocument.xml</gco:CharacterString>
	</gmd:fileIdentifier>
	<gmd:language>
		<gco:CharacterString>eng; CAN</gco:CharacterString>
	</gmd:language>
	<gmd:characterSet>
		<gmd:MD_CharacterSetCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode" codeListValue="utf8" codeSpace="ISOTC211/19115">utf8</gmd:MD_CharacterSetCode>
	</gmd:characterSet>
	<gmd:contact>
		<gmd:CI_ResponsibleParty>
			<gmd:individualName>
				<gco:CharacterString>John Doe</gco:CharacterString>
			</gmd:individualName>
			<gmd:organisationName>
				<gco:CharacterString>ACME Corporation</gco:CharacterString>
			</gmd:organisationName>
			<gmd:contactInfo>
				<gmd:CI_Contact>
					<gmd:phone>
						<gmd:CI_Telephone>
							<gmd:voice>
								<gco:CharacterString>(000) 123-456-7890</gco:CharacterString>
							</gmd:voice>
						</gmd:CI_Telephone>
					</gmd:phone>
					<gmd:address>
						<gmd:CI_Address>
							<gmd:deliveryPoint>
								<gco:CharacterString>42 Wallaby Way</gco:CharacterString>
							</gmd:deliveryPoint>
							<gmd:city>
								<gco:CharacterString>Sydney</gco:CharacterString>
							</gmd:city>
							<gmd:administrativeArea>
								<gco:CharacterString>New South Wales</gco:CharacterString>
							</gmd:administrativeArea>
							<gmd:postalCode>
								<gco:CharacterString>123000</gco:CharacterString>
							</gmd:postalCode>
							<gmd:country>
								<gco:CharacterString>Sealand</gco:CharacterString>
							</gmd:country>
							<gmd:electronicMailAddress>
								<gco:CharacterString>helloworld@example.org</gco:CharacterString>
							</gmd:electronicMailAddress>
						</gmd:CI_Address>
					</gmd:address>
				</gmd:CI_Contact>
			</gmd:contactInfo>
			<gmd:role>
				<gmd:CI_RoleCode codeList="http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode" codeListValue="pointOfContact" codeSpace="ISOTC211/19115">pointOfContact</gmd:CI_RoleCode>
			</gmd:role>
		</gmd:CI_ResponsibleParty>
	</gmd:contact>
	<gmd:dateStamp>
		<gco:Date>1970-01-01</gco:Date>
	</gmd:dateStamp>
	<gmd:identificationInfo>
		<gmd:MD_DataIdentification>
			<gmd:language>
				<gco:CharacterString>eng; CAN</gco:CharacterString>
			</gmd:language>
			<gmd:topicCategory>
				<gmd:MD_TopicCategoryCode>life</gmd:MD_TopicCategoryCode>
			</gmd:topicCategory>
			<gmd:extent>
				<gmd:EX_Extent id="boundingExtent">
					<gmd:geographicElement>
						<gmd:EX_GeographicBoundingBox id="boundingGeographicBoundingBox">
							<gmd:westBoundLongitude>
								<gco:Decimal>-180</gco:Decimal>
							</gmd:westBoundLongitude>
							<gmd:eastBoundLongitude>
								<gco:Decimal>-90</gco:Decimal>
							</gmd:eastBoundLongitude>
							<gmd:southBoundLatitude>
								<gco:Decimal>180</gco:Decimal>
							</gmd:southBoundLatitude>
							<gmd:northBoundLatitude>
								<gco:Decimal>90</gco:Decimal>
							</gmd:northBoundLatitude>
						</gmd:EX_GeographicBoundingBox>
					</gmd:geographicElement>
					<gmd:temporalElement>
						<gmd:EX_TemporalExtent>
							<gmd:extent>
								<gml:TimePeriod gml:id="boundingTemporalExtent">
									<gml:beginPosition>1970-01-01</gml:beginPosition>
									<gml:endPosition>2020-12-31</gml:endPosition>
								</gml:TimePeriod>
							</gmd:extent>
						</gmd:EX_TemporalExtent>
					</gmd:temporalElement>
				</gmd:EX_Extent>
			</gmd:extent>
		</gmd:MD_DataIdentification>
	</gmd:identificationInfo>
</gmd:MD_Metadata>

```
#### Turtle Output
```
@prefix gmd: <http://www.isotc211.org/2005/gmd#> .
@prefix gml: <http://www.opengis.net/gml#> .

[] a gmd:MD_Metadata ;
    gmd:characterSet "utf8" ;
    gmd:codeList "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#MD_CharacterSetCode" ;
    gmd:codeListValue "utf8" ;
    gmd:codeSpace "ISOTC211/19115" ;
    gmd:contact [ a gmd:CI_ResponsibleParty ;
            gmd:codeList "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode" ;
            gmd:codeListValue "pointOfContact" ;
            gmd:codeSpace "ISOTC211/19115" ;
            gmd:contactInfo [ a gmd:CI_Contact ;
                    gmd:address [ a gmd:CI_Address ;
                            gmd:administrativeArea "New South Wales" ;
                            gmd:city "Sydney" ;
                            gmd:country "Sealand" ;
                            gmd:deliveryPoint "42 Wallaby Way" ;
                            gmd:electronicMailAddress "helloworld@example.org" ;
                            gmd:postalCode "123000" ] ;
                    gmd:phone [ a gmd:CI_Telephone ;
                            gmd:voice "(000) 123-456-7890" ] ] ;
            gmd:individualName "John Doe" ;
            gmd:organisationName "ACME Corporation" ;
            gmd:role "pointOfContact" ] ;
    gmd:dateStamp "1970-01-01" ;
    gmd:fileIdentifier "myXMLDocument.xml" ;
    gmd:identificationInfo [ a gmd:MD_DataIdentification ;
            gmd:extent [ a gmd:EX_Extent ;
                    gmd:geographicElement [ a gmd:EX_GeographicBoundingBox ;
                            gmd:eastBoundLongitude "-90" ;
                            gmd:northBoundLatitude "90" ;
                            gmd:southBoundLatitude "180" ;
                            gmd:westBoundLongitude "-180" ] ;
                    gmd:id "boundingGeographicBoundingBox" ;
                    gmd:temporalElement [ a gmd:EX_TemporalExtent ;
                            gmd:extent [ a gml:TimePeriod ;
                                    gml:beginPosition "1970-01-01" ;
                                    gml:endPosition "2020-12-31" ] ] ] ;
            gmd:id "boundingExtent" ;
            gmd:language "eng; CAN" ;
            gmd:topicCategory "life" ] ;
    gmd:language "eng; CAN" .
```