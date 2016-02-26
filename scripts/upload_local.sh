#yes local is 3001


TODAY="16-12-2015" &&
#TODAY=$(date +"%d-%m-%Y") &&
mongoimport -h localhost:3001 --db meteor --collection articles --type json --file private/test.json --jsonArray &&
echo 'imported files to local'  

#run on port 3003
 
