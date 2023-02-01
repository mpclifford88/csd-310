from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.4apea7f.mongodb.net/pytech?retryWrites=true&w=majority"

client = MongoClient(url)

db = client.pytech

students = db.students

student_list = students.find({})

print("\n  -- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")

for doc in student_list:
    print("  Student ID: " + doc["student_id"] + "\n  First Name: " + doc["first_name"] + "\n  Last Name: " + doc["last_name"] + "\n")

#Matt
result = students.update_one({"student_id": "1007"}, {"$set": {"last_name": "Clifford Jr."}})

matt = students.find_one({"student_id": "1007"})

print("\n  -- DISPLAYING STUDENT DOCUMENT 1007 --")

print("  Student ID: " + matt["student_id"] + "\n  First Name: " + matt["first_name"] + "\n  Last Name: " + matt["last_name"] + "\n")
 
input("\n\n  End of program, press any key to continue...")
