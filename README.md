### Movie social media
A movie social media with python, Neo4j and Tkinter.

Project for NoSQL course, spring 2017, Shabid Beheshti University.

Administrative features:
* adding movies and tv shows
* adding news

User features:
* editing user info.
* having friends list
* rating movies
* having a list of watched movies
* search movies/tv shows
* add movies/tv shows

Friend recommendation criteria (recommendation.py):
* two users have at least 3 mutual friends
* have watched same movies and given same ratings

Movie recommendation criteria to user _x_ (mr.py):
* movies with genres similar to user _x_ liked movies
* movies/shows liked by other users who like the same things as user _x_
* movies/shows liked by other users who have the same age, gender and education of user _x_
