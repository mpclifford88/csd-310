from pymongo import MongoClient

url = "mongodb+srv://admin:admin@cluster0.4apea7f.mongodb.net/pytech?retryWrites=true&w=majority"

client = MongoClient(url)

db = client.pytech

students = db.students

student_list = students.find({})

print("\n  -- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")

for doc in student_list:
    print("  Student ID: " + doc["student_id"] + "\n  First Name: " + doc["first_name"] + "\n  Last Name: " + doc["last_name"] + "\n")

billy = {
    "student_id": "1010",
    "first_name": "Billy",
    "last_name": "Bob"
}

billy = students.insert_one(billy).inserted_id

print("\n  -- INSERT STATEMENTS --")
print("  Inserted student record into the students collection with document_id " + str(billy))

student_billy = students.find_one({"student_id": "1010"})

print("\n  -- DISPLAYING STUDENT TEST DOC -- ")
print("  Student ID: " + student_billy["student_id"] + "\n  First Name: " + student_billy["first_name"] + "\n  Last Name: " + student_billy["last_name"] + "\n")

deleted_student_test_doc = students.delete_one({"student_id": "1010"})

new_student_list = students.find({})

print("\n  -- DISPLAYING STUDENTS DOCUMENTS FROM find() QUERY --")

for doc in new_student_list:
    print("  Student ID: " + doc["student_id"] + "\n  First Name: " + doc["first_name"] + "\n  Last Name: " + doc["last_name"] + "\n")

input("\n\n  End of program, press any key to continue...")