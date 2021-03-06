# Todo

## Backend
 
 - `create_test_ontologies`: 
    - Add local_name management
        -  Create an example
    - Add Forms and fields
    - Make the script run with pyramid configuration
    - Write the files in /db
 
 - Reliability: add try / except statements to services in order to format exception
   properly and close connections
  
 - DateInput: convert to date instead of string

## Frontend
 
 - **Form Validation**
 - **SubForm**
 - Make "new individual" working
 - Make "delete" in "individuals list" working

## Generic

 - Ontology:
    - Submit birda to w3id
    - Check '/' instead of '#'
    - Add "hasBaseURI"
    - Add "hasLocalName"
        - Add child "hasLocalNameFields"
            - Comma separated URIs
        - Add child "hasLocalNameSeparator"
        - Add child "hasLocalNameTokenSeparator"
        - Add child "hasLocalNameRenderer"
	- Add "hasReferenceForm"
	    - Only for SubForms
	    - States what is the preferred form for inserting elements

## Widgets

 - (x) /TextInput
 - ( ) /TextAreaInput
 - (x) /CheckboxInput
 - (x) /DateInput
 - ( ) /NumberInput
 - ( ) /RadioInput
 - ( ) /SelectInput
 - ( ) /StaticText
 - ( ) /SubForm
 - ( ) /TabbedFieldSet
 - ( ) /NextFieldSet


## Low Priority

 - Create test ontologies
 - make run-fe Production
 
## Maybe next steps

### Features

 - Authentication
 - Authorization
 - Multilanguage on frontend
 - Individuals authors
 - Individuals modified time
 - Other output formats besides json (e.g. turtle, nt, etc.)
 - Storage on other databases besides files
 - Implementing RDFA in frontend
 - Fields autocomplete

 - Validation of produced individuals
 - Facilitated creation of birda widgets
 - Unittests

### Improvements
 - Backend: Proper caching of form widget by the form_factory for large number of forms
 - Backend / Frontend: communications between backend and fontend are currently
   managed by a belt and braces mix of CORS and xdomain. This should be rationalized 
   and simplified.

### Performance
 - Backend: lazy loading individual (and forms?) translations form db
 - Backend: reduce db accesses by taking advance from data already at hand