-- View all students
SELECT * FROM students;

-- Update marks
UPDATE students
SET marks = 95
WHERE id = 1;

-- Delete a student
DELETE FROM students
WHERE id = 2;

COMMIT;
