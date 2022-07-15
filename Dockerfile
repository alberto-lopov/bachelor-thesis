FROM arangodb

EXPOSE 8529

#Enviromental variables for authorization in DB
#Auth is disable, it doesn't matter, this is a local project and we are not managing sensible data
ENV ARANGO_NO_AUTH=1

#To build this docker file (-t is used to name the build)
# docker build -t="arangodb/final-grade-project" .

#To run a container with a built image and specifying the volume where you are going to store it (absolute path this case is windows)
# docker run -d -p 8529:8529 -v C:\Users\Alberto_Work\Desktop\TFG\finalGradeProject\data-db:/var/lib/arangodb3 --name arango_finalGradeProject arangodb/final-grade-project