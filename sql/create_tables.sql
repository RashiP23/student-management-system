-- Drop table if exists (ignore error if table not found)
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE students';
EXCEPTION
   WHEN OTHERS THEN
      NULL;
END;
/

-- Drop sequence if exists
BEGIN
   EXECUTE IMMEDIATE 'DROP SEQUENCE student_seq';
EXCEPTION
   WHEN OTHERS THEN
      NULL;
END;
/

-- Create table
CREATE TABLE students (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(50),
    age NUMBER,
    course VARCHAR2(50),
    marks NUMBER
);

-- Create sequence for auto ID
CREATE SEQUENCE student_seq
START WITH 1
INCREMENT BY 1;

COMMIT;
