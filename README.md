## Name
Teachers Help Teachers

## Description
The goal of this project is to create a public, open source resource for computer science educators to be able to create and share practice programming questions. These questions will be in the form of templates created by our end-users — computer science teachers — with the intention of being shared with other teachers. Each question template will contain aspects that can be randomized within given parameters meaning that each question template can provide multiple practice programming problems for students over a given topic. Teachers will be able to browse the entries of their peers and draw from them to create assignments and assessments to use themselves. 


## Visuals


## Installation
This application runs on Python 3
```bash
pip install python3
```
This application uses two environmental variables that will have to have values copied and pasted in.
For Linux or MacOS:
```bash
export GOOGLE_CLIENT_ID=copy and paste ID
export GOOGLE_CLIENT_SECRET=copy and paste secret
```
For Windows:
```bash
set GOOGLE_CLIENT_ID=copy and paste ID
set GOOGLE_CLIENT_SECRET=copy and paste secret
```
To run the application, use flask with a HTTPS connection.
```bash
flask run --cert=adhoc
```

## Usage


## Support


## Roadmap


## Contributing


## License 


## Release Notes
6-24 

  -Preview question is working. We can navigate between screens. Everything has a location that backend code can be deposited into.

7-15 

  -Users can enter question templates, view previews of randomized parameters for their templates or see if an error occurred
  
  -Users can push questions templates to the database. Each template has an associated auther (based on the user's email for login) and category entered by the user in a textbox
  
  -Users can get questions from the database with the randomized parameters filled in. Questions can be retrieved with the filters of author, category, both, or neither
  
  -Navigation bar added
