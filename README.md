## Name
Teachers Help Teachers

## Description
As a computer science educator, for each topic that you cover for your students you need a robust range of practice materials for the students to hone their skills and demonstrate full understanding of the topic. Often this means that each teacher must create many practice questions that are similar to each other to give the students assignments, practice for assessments, and then the assessments themselves. This can be onerous on an individual teacher who doesn’t have access to resources to draw questions from. 


The goal of this project was to create a public, open source resource for computer science educators to be able to create and share practice programming questions. These questions will be in the form of templates created by our end-users — computer science teachers — with the intention of being shared with other teachers. Each question template will contain aspects that can be randomized within given parameters meaning that each question template can provide multiple practice programming problems for students over a given topic. Teachers will be able to browse the entries of their peers and draw from them to create assignments and assessments to use themselves. 


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


## Project Status

## Release Notes
The entire application is working with all features behaving according to the 
user stories and automated test available to verify all application routes.
The next step to be done is to deploy the app on Heroku.
