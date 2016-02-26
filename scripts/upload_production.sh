
#TODAY='01-12-2015' &&
#CMD=`meteor mongo -U sortinghatnews.meteor.com | tail -1 | sed 's_mongodb://\([a-z0-9\-]*\):\([a-f0-9\-]*\)@\(.*\)/\(.*\)_mongoimport -u \1 -p \2 -h \3 -d \4 -c articles --type json --jsonArray_'` &&

#$CMD data/$TODAY/$TODAY-CLEAN.json &&
#echo 'imported files to production'


TODAY='01-12-2015' &&
CMD=`meteor mongo -U readingroom.meteor.com | tail -1 | sed 's_mongodb://\([a-z0-9\-]*\):\([a-f0-9\-]*\)@\(.*\)/\(.*\)_mongoimport -u \1 -p \2 -h \3 -d \4 -c articles --type json --jsonArray_'` &&

$CMD private/test.json &&
echo 'imported files to production'