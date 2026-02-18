from db_config import get_connection

def add_student():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    course = input("Enter course: ")
    marks = int(input("Enter marks: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO students
        VALUES (student_seq.NEXTVAL, :1, :2, :3, :4)
    """, (name, age, course, marks))

    conn.commit()
    cur.close()
    conn.close()

    print("Student added successfully!")


def view_students():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    print("\nID  NAME   AGE  COURSE  MARKS")
    print("--------------------------------")
    for r in rows:
        print(r)

    cur.close()
    conn.close()


def update_marks():
    sid = int(input("Enter student ID: "))
    marks = int(input("Enter new marks: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE students SET marks = :1 WHERE id = :2",
        (marks, sid)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Marks updated successfully!")


def delete_student():
    sid = int(input("Enter student ID to delete: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id = :1", (sid,))
    conn.commit()

    cur.close()
    conn.close()

    print("Student deleted successfully!")


while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Marks")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        update_marks()
    elif choice == "4":
        delete_student()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
