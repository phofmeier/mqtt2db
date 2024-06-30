from pymongo import MongoClient

def get_database():

    # Geben Sie die MongoDB Atlas-URL ein, um Python unter Verwendung von pymongo mit MongoDB zu verbinden
    CONNECTION_STRING = "localhost:27017"

    # Erstellen Sie eine Verbindung mit MongoClient. Sie können MongoClient importieren oder pymongo.MongoClient verwenden
    client = MongoClient(CONNECTION_STRING)

    # Erstellen Sie die Datenbank für unser Beispiel (wir verwenden im gesamten Tutorial dieselbe Datenbank
    return client['test_db']
  
# Dies wird hinzugefügt, damit viele Dateien die Funktion get_database() wiederverwenden können
if __name__ == "__main__":   
   # Datenbank abrufen
   dbname = get_database()
   collection = dbname["test_collection"]

   test_item = {
       "_id" : "001",
  "item_name" : "test_1",
   "item_val" : 10.1,
 
}
   collection.insert_one(test_item)


   print(collection.find_one())