db = db.getSiblingDB('movies') ;
db.createCollection('likes');
db.createCollection('reviews');
db.createCollection('bookmarks');
