-- CMSC 127 ST26L Milestone 3
-- MySJL - Chan, Germinal, Mariquit
-- After the creation of the entity relationship diagram and the relational tables, these are the SQL statements for the creation of our final app project in CMSC 127. The SQL queries are separated into CRUD (Create, Read, Update, Delete)

-- RELATIONAL TABLES
-- ORGANIZATION (_Organization id_, Name)
-- MEMBER(_Student number_, First name, Last name, Middle name, Gender, Degree program)
-- JOINS(_Student number_, _Organization id_, _Academic year_, _Semester_, _Role_, _Status_)
-- MEMBER_BATCH(_Student number_, _Organization id_, Batch)
-- COMMITTEE(_Committee name_, _Organization id_, Semester, Academic year)
-- COMMITTEE_ROLE(_Committee name_, _Organization id_, Role)
-- STUDENT_ROLE(_Student number_, _Organization id_, _Committee name_, Role)
-- FEE(_Organization id_, _Student number_, _Fee name_, Due date, Academic year, Status, Semester, Amount)
-- PAYMENT(_Fee name_, _Student number_, _Organization id_, _Full payment date_, _Due date_, Is payment late)

-- questions - should we keep text fields to a standard 128 or better to adjust based on their capability?
-- notes:
-- Role and status is actually a reserver keyword in SQL
-- When a PRIMARY KEY constraint is added, it is automatically UNIQUE

-- CONSTRAINT UK_Joins UNIQUE KEY (StudentNumber, OrganizationId, AcademicYear, Semester)
-- This means that UNIQUE KEY constraint, named UK_Joins, means that the combination of the values in the StudentNumber, OrganizationId, AcademicYear, and Semester columns must be unique across all rows in the table. It does not mean that each individual attribute (StudentNumber, OrganizationId, AcademicYear, Semester) must be unique on its own. Same goes sa primary key
-- An attribute that was put in the primary key constraint cannot be separately put in a unique key constraint

-- CREATE STATEMENTS
-- Should I set the varchars as a constant 128 or should I set it to a reasonable character count based on what the string is for?
-- stimmie: I feel like we should have foreign keys. I'll ask Ma'am Mira if pwedeng mag-deviate sa Milestone 2.
-- stimmie: apparently the primary key cannot be named in mysql???

CREATE USER 'organizationer'@'localhost' IDENTIFIED BY 'uplbsqlsociety';
CREATE DATABASE IF NOT EXISTS organization;
GRANT CREATE, UPDATE, DROP, DELETE, INSERT, SELECT ON organization.* TO 'organizationer'@'localhost';
USE organization;

CREATE TABLE organization (
    `Organization ID` int NOT NULL,
    `Organization Name` varchar(128),
    CONSTRAINT PK_Organization PRIMARY KEY (`Organization ID`)
);

INSERT INTO organization(`Organization ID`, `Organization Name`) VALUES 
('11111111', 'Malayang Asosasyon ng Shih Tzu at Siberian Husky'),
('22222222', 'Circle of Secretive Species'),
('33333333', 'Alliance of Cat Students for Science'),
('44444444', 'Young Squirrel Entrepreneurial Society'),
('55555555', 'Cats, Penguins, and Sloths Triad');

CREATE TABLE member (
    `Student Number` varchar(128) NOT NULL,
    `First Name` varchar(128) NOT NULL,
    `Middle Name` varchar(128), -- some ppl have no middle name
    `Last Name` varchar(128) NOT NULL,
    `Gender` varchar(128), 
    `Degree Program` varchar(128),
    CONSTRAINT PK_Member PRIMARY KEY (`Student Number`)
);

INSERT INTO member(`Student Number`, `First Name`, `Middle Name`, `Last Name`, `Gender`, `Degree Program`) VALUES
('20230001', 'Luna', 'B.', 'Meowington', 'Female', 'BS Zoology'),
('20230002', 'Barkley', NULL, 'Howlson', 'Male', 'BS Computer Science'),
('20230003', 'Otto', 'J.', 'Riverpaw', 'Male', 'BS Environmental Science'),
('20230004', 'Gerry', 'K.', 'Neckson', 'Nonbinary', 'BS Architecture'),
('20230005', 'Tina', 'M.', 'Shellford', 'Female', 'BS Marine Biology');

CREATE TABLE joins (
    `Student Number` varchar(128) NOT NULL ,
    `Organization ID` int NOT NULL,
    `Academic Year` varchar(128) NOT NULL,
    `Semester` varchar(128) NOT NULL,
    `Member Role` varchar(128) NOT NULL,
    `Member Status` varchar(128) NOT NULL,
    CONSTRAINT PK_Joins PRIMARY KEY (`Student Number`, `Organization ID`, `Academic Year`, `Semester`),
    CONSTRAINT UQ_SN UNIQUE (`Student Number`) -- wait what if hindi nag eexist yung S/N sa Member table? wala bang constraint for that? why wouldnt it exist there lahat naman ng member may std no
);

INSERT INTO joins(`Student Number`, `Organization ID`, `Academic Year`, `Semester`, `Member Role`, `Member Status`) VALUES
('20230001', 11111111, '2024-2025', '1st', 'President', 'Active'),
('20230002', 22222222, '2024-2025', '1st', 'Treasurer', 'Active'),
('20230003', 33333333, '2024-2025', '2nd', 'Member', 'Inactive'),
('20230004', 44444444, '2024-2025', '1st', 'Secretary', 'Active'),
('20230005', 55555555, '2024-2025', '1st', 'Member', 'Probation');

CREATE TABLE member_batch (
    `Student Number` varchar(128) NOT NULL,
    `Organization ID` int NOT NULL,
    `Batch` int NOT NULL, 
    CONSTRAINT PK_Joins PRIMARY KEY(`Student Number`, `Organization ID`, `Batch`) -- Makes more sense na a student can only have one batch kaya kasama siya dapat sa primary key
);

INSERT INTO member_batch(`Student Number`, `Organization ID`, `Batch`) VALUES
('20230001', 11111111, 2023),
('20230002', 22222222, 2022),
('20230003', 33333333, 2021),
('20230004', 44444444, 2023),
('20230005', 55555555, 2024);

CREATE TABLE student_role(
    `Student Number` varchar(128) NOT NULL, 
    `Organization ID` int NOT NULL,
    `Committee Name` varchar(128) NOT NULL,
    `Role` varchar(128) NOT NULL,
    CONSTRAINT PK_Joins PRIMARY KEY(`Student Number`, `Organization ID`, `Committee Name`) 
);

INSERT INTO student_role(`Student Number`, `Organization ID`, `Committee Name`, `Role`) VALUES
('20230001', 11111111, 'Snack Patrol', 'Snackmaster'),
('20230002', 22222222, 'Fundraising Ferrets', 'Finance Head'),
('20230003', 33333333, 'Otter Awareness', 'Public Relations'),
('20230004', 44444444, 'Tall Talks', 'Moderator'),
('20230005', 55555555, 'Shell Squad', 'Logistics');

CREATE TABLE committee (
    `Committee Name` varchar(128) NOT NULL,
    `Organization ID` int NOT NULL,
    `Semester` varchar(128) NOT NULL,
    `Academic Year` varchar(128) NOT NULL,
    CONSTRAINT PK_Committee PRIMARY KEY(`Committee Name`, `Organization ID`)
);

INSERT INTO committee(`Committee Name`, `Organization ID`, `Semester`, `Academic Year`) VALUES
('Snack Patrol', 11111111, '1st', '2024-2025'),
('Fundraising Ferrets', 22222222, '1st', '2024-2025'),
('Otter Awareness', 33333333, '2nd', '2024-2025'),
('Tall Talks', 44444444, '1st', '2024-2025'),
('Shell Squad', 55555555, '1st', '2024-2025');

CREATE TABLE committee_role (
    `Committee Name` varchar(128) NOT NULL,
    `Organization ID` int NOT NULL,
    `Role` varchar(128) NOT NULL,
    CONSTRAINT PK_CommitteeRole PRIMARY KEY(`Committee Name`, `Organization ID`, `Role`) -- If a committee can have multiple roles, the primary key should include the `Role` as well.
);

INSERT INTO committee_role(`Committee Name`, `Organization ID`, `Role`) VALUES
('Snack Patrol', 11111111, 'Snackmaster'),
('Fundraising Ferrets', 22222222, 'Finance Head'),
('Otter Awareness', 33333333, 'Public Relations'),
('Tall Talks', 44444444, 'Moderator'),
('Shell Squad', 55555555, 'Logistics');

CREATE TABLE fee(
    `Organization ID` int NOT NULL,
    `Student Number` varchar(128) NOT NULL,
    `Fee Name` varchar(128) NOT NULL,
    `Due Date` date NOT NULL,
    `Academic Year` varchar(128) NOT NULL,
    `Status` varchar(128) NOT NULL,
    `Semester` varchar(128) NOT NULL,
    `Amount` varchar(128) NOT NULL,
    CONSTRAINT PK_Fee PRIMARY KEY(`Fee Name`, `Student Number`, `Organization ID`, `Academic Year`, `Semester`) -- Academic year and semester might be more logical to add to the PK
);
INSERT INTO fee(`Organization ID`, `Student Number`, `Fee Name`, `Due Date`, `Academic Year`, `Status`, `Semester`, `Amount`) VALUES
(11111111, '20230001', 'Annual Dues', '2024-10-01', '2024-2025', 'Pending', '1st', '300'),
(22222222, '20230002', 'Event Fee', '2024-09-15', '2024-2025', 'Paid', '1st', '150'),
(33333333, '20230003', 'Otter Field Trip', '2025-01-10', '2024-2025', 'Unpaid', '2nd', '500'),
(44444444, '20230004', 'Poster Printing', '2024-11-05', '2024-2025', 'Paid', '1st', '100'),
(55555555, '20230005', 'Turtle Shell Care', '2024-12-12', '2024-2025', 'Pending', '1st', '250');


CREATE TABLE payment(
    `Fee Name` varchar(128) NOT NULL,
    `Student Number` varchar(128) NOT NULL,
    `Organization ID` int NOT NULL,
    `Full Payment Date` date NOT NULL,
    `Due Date` date NOT NULL,
    `Payment Late?` boolean NOT NULL,
    CONSTRAINT PK_Payment PRIMARY KEY(`Fee Name`, `Student Number`, `Organization ID`, `Full Payment Date`) -- Maybe hindi na need ng Due Date to uniquely identify a payment record
);

INSERT INTO payment(`Fee Name`, `Student Number`, `Organization ID`, `Full Payment Date`, `Due Date`, `Payment Late?`) VALUES
('Annual Dues', '20230001', 11111111, '2024-10-02', '2024-10-01', TRUE),
('Event Fee', '20230002', 22222222, '2024-09-10', '2024-09-15', FALSE),
('Otter Field Trip', '20230003', 33333333, '2025-01-15', '2025-01-10', TRUE),
('Poster Printing', '20230004', 44444444, '2024-11-04', '2024-11-05', FALSE),
('Turtle Shell Care', '20230005', 55555555, '2024-12-10', '2024-12-12', FALSE);


-- 1. View all members of the organization by role, status, gender, degree program, batch (year of membership), and committee. (Note: we assume one committee membership only per organization per semester) 
CREATE OR REPLACE VIEW membersvu(student_number, last_name, first_name, role, status, gender, degree_program, batch, committee)
    AS SELECT m.`Student Number`, m.`Last Name`, m.`First Name`, 
        sr.`Role`, j.`Member Status`, m.`Gender`, m.`Degree Program`, 
        mb.`Batch`, sr.`Committee Name`
    FROM member m
    JOIN member_batch mb 
        ON m.`Student Number` = mb.`Student Number` 
    JOIN student_role sr 
        ON m.`Student Number` = sr.`Student Number`
        AND mb.`Organization ID` = sr.`Organization ID`
    JOIN joins j 
        ON m.`Student Number` = j.`Student Number`
        AND j.`Organization ID` = sr.`Organization ID`
    WHERE sr.`Organization ID` = 11111111;


-- 2. View members for a given organization with unpaid membership fees or dues for a given semester and academic year. WORKING
CREATE OR REPLACE VIEW unpaid_fees_orgvu(organization_id, student_number, last_name, first_name, fee_name, amount, due_date, status)
    AS SELECT f.`Organization ID`, m.`Student Number`, m.`Last Name`, m.`First Name`, f.`Fee Name`, f.`Amount`, f.`Due Date`, f.`Status`
    FROM member m
    JOIN fee f ON m.`Student Number` = f.`Student Number`
    WHERE f.`Status` = 'Unpaid'
    AND f.`Organization ID` = 11111111
    AND f.`Academic Year` = '2024-2025'
    AND f.`Semester` = '1st';


-- 3. View a member's unpaid membership fees or dues for all their organizations (Member's POV). 
CREATE OR REPLACE VIEW unpaid_fees_membervu(student_number, organization_id, fee_name, amount, due_date, academic_year, semester)
    AS SELECT f.`Student Number`, f.`Organization ID`, f.`Fee Name`, f.`Amount`, f.`Due Date`, f.`Academic Year`, f.`Semester`
    FROM fee f
    WHERE f.`Status` = 'Unpaid';
    
    -- specify which student when viewing view, ex:
        -- SELECT * FROM unpaid_fees_membervu
        -- WHERE student_number = '20230001';


-- 4. View all executive committee members of a given organization for a given academic year. 
CREATE OR REPLACE VIEW executive_committee_membersvu(student_number, last_name, first_name, committee_name, semester)
    AS SELECT m.`Student Number`, m.`Last Name`, m.`First Name`, sr.`Committee Name`, c.`Semester`
    FROM member m
    JOIN student_role sr ON m.`Student Number` = sr.`Student Number`
    JOIN committee c ON sr.`Committee Name` = c.`Committee Name`
        AND sr.`Organization ID` = c.`Organization ID`
    WHERE sr.`Organization ID` = 11111111
    AND c.`Academic Year` = '2024-2025'
    AND c.`Committee Name` = 'Executive';


-- 5. View all Presidents (or any other role) of a given organization for every academic year in reverse chronological order (current to past).
CREATE OR REPLACE VIEW organization_rolevu(student_number, last_name, first_name, role, academic_year)
    AS SELECT m.`Student Number`, m.`Last Name`, m.`First Name`, j.`Member Role`, j.`Academic Year`
    FROM member m
    JOIN joins j ON m.`Student Number` = j.`Student Number`
    WHERE j.`Member Role` = 'President'
        AND j.`Organization ID` = 11111111
    ORDER BY STR_TO_DATE(CONCAT(SUBSTRING_INDEX(j.`Academic Year`, '-', 1), '-01-01'), '%Y-%m-%d') DESC;


-- 6. View all late payments made by all members of a given organization for a given semester and academic year. 
CREATE OR REPLACE VIEW late_paymentsvu(fee_name, student_number, organization_id, due_date, payment_late?)
    AS SELECT f.`Fee Name`, f.`Student Number`, f.`Organization ID`, f.`Due Date`, f.`Payment Late?`
    FROM fee f
    JOIN joins j ON f.`Student Number` = j.`Student Number`
    WHERE f.`Organization ID` = 11111111;
        AND f.`Payment Late?` = TRUE;
        AND j.`Academic Year` = "2024-2025";
        AND j.`Semester` = "1st";


-- 7. View the percentage of active vs inactive members of a given organization for the last n semesters. (Note: n is a positive integer)
 


-- 8. View all alumni members of a given organization as of a given date.
CREATE OR REPLACE VIEW alumnivu(student_number, first_name, last_name, organization_id, status) 
    AS SELECT m.`Student Number`, m.`First Name`, m.`Last Name`, j,`Organization ID`, j.`Status`
    FROM member m
    JOIN joins j ON m.`Student Number` = j.`Student Number`
    WHERE j.`Organization ID` = 11111111;
        AND j.`Status` = "Alumni";  -- not sure if dito makikita if alumni



-- 9. View the total amount of unpaid and paid fees or dues of a given organization as of a given date. 
CREATE OR REPLACE VIEW org_feesvu(organization_name, organization_id, fee_name, amount, due_date, academic_year, semester)
    AS SELECT o.`Name`, o.`Organization ID`, f.`Fee Name`, f.`Amount`, f.`Due Date`, f.`Academic Year`, f.`Semester`
    FROM organization m
    JOIN fee f ON m.`Organization ID` = f.`Organization ID`
    WHERE m.`Organization ID` = 11111111
        AND 


-- 10. View the member/s with the highest debt of a given organization for a given semester. 
CREATE OR REPLACE VIEW high_debtsvu(fee_name, student_number, organization_id, due_date, amount, status)
    AS SELECT f.`Fee Name`, f.`Student Number`, f.`Organization ID`, f.`Due Date`, f.`Amount`, f.`Status`
    FROM fee f
    JOIN joins j ON f.`Student Number` = j.`Student Number`
    WHERE f.`Organization ID` = 11111111
        AND f.`Status` = "Unpaid"
        AND j.`Academic Year` = "2024-2025"
        AND j.`Semester` = "1st"
    ORDER BY f.`Amount` DESC;


-- update student role 
UPDATE student_role 
    SET `Role` = "Snackeater"
    WHERE `Organization ID` = 11111111
        AND `Student Number` = "20230001"
        AND `Committee Name` = "Snack Patrol";

-- update organization name
UPDATE organization 
    SET `Name` = "Society of Societies"
    WHERE `Organization ID` = 11111111;

-- update committee role
UPDATE committee_role  
    SET `Role` = "Snackeater"
    WHERE `Organization ID` = 11111111
        AND `Committee Name` = "Snack Patrol";


-- update membership status
UPDATE joins 
    SET `Status` = "Inactive"
    WHERE `Student Number` = 20230001
        AND `Organization ID` = 11111111
        AND `Academic Year` = "2024-2025"
        AND `Semester` = "1st"

-- update fee status
UPDATE fee
    SET `Status` = "Paid"
    WHERE `Fee Name` = "Annual Dues"
        AND `Student Number` = 20230001
        AND `Organization ID` = 11111111
        AND `Academic Year` = 2024-2025
        AND `Semester`= 1st

-- update fee due date
UPDATE fee
    SET `Due Date` = "2024-11-11"
    WHERE `Fee Name` = "Annual Dues"
        AND `Student Number` = 20230001
        AND `Organization ID` = 11111111
        AND `Academic Year` = 2024-2025
        AND `Semester`= 1st


-- update full payment date
UPDATE payment
    SET `Full Payment Date` = "2024-11-11"
    WHERE `Fee Name` = "Annual Dues"
        AND `Student Number` = 20230001
        AND `Organization ID` = 11111111
        AND `Full Payment Date` = '2024-10-02'

-- update payment late?
UPDATE payment
    SET `Payment Late?` = FALSE
    WHERE `Fee Name` = "Annual Dues"
        AND `Student Number` = 20230001
        AND `Organization ID` = 11111111
        AND `Full Payment Date` = "2024-11-11"

-- update due date
UPDATE payment
    SET `Due Date` = "2024-12-12"
    WHERE `Fee Name` = "Annual Dues"
        AND `Student Number` = 20230001
        AND `Organization ID` = 11111111
        AND `Full Payment Date` = "2024-11-11"

-- delete member from database
DELETE FROM member 
    WHERE `Student Number` = 20230001;
DELETE FROM joins 
    WHERE `Student Number` = 20230001 
        AND `Organization ID` = 11111111;
DELETE FROM member_batch 
    WHERE `Student Number` = 20230001
        AND `Organization ID` = 11111111;
DELETE FROM student_role 
    WHERE `Student Number` = 20230001
        AND `Organization ID` = 11111111;
DELETE FROM fee 
    WHERE `Student Number` = 20230001
        AND `Organization ID` = 11111111;
DELETE FROM payment 
    WHERE `Student Number` = 20230001
        AND `Organization ID` = 11111111;

-- delete fee from database
DELETE FROM fee
    WHERE `Fee Name` = "Otter Field Trip"
        AND `Organization ID` = 33333333;


-- delete member payment from database
DELETE FROM payment
    WHERE `Fee Name` = "Poster Printing"
        AND `Organization ID` = 44444444
        AND `Student Number` = "20230004";



-- NOT SURE IF INCLUDED IN MILESTONE

-- update student number
-- UPDATE member 
--     SET `Student Number` = 20231111
--     WHERE `Student Number` = 20230001;

-- UPDATE joins 
--     SET `Student Number` = 20231111
--     WHERE `Student Number` = 20230001
--         AND `Organization ID` = 11111111;

-- UPDATE member_batch 
--     SET `Student Number` = 20231111
--     WHERE `Student Number` = 20230001
--         AND `Organization ID` = 11111111;

-- UPDATE student_role 
--     SET `Student Number` = 20231111
--     WHERE `Student Number` = 20230001
--         AND `Organization ID` = 11111111;

-- UPDATE fee
--     SET `Student Number` = 20231111
--     WHERE `Student Number` = 20230001
--         AND `Organization ID` = 11111111;

-- UPDATE payment 
--     SET `Student Number` = 20231111
--     WHERE `Student Number` = 20230001
--         AND `Organization ID` = 11111111;


-- -- update first name
-- UPDATE member 
--     SET `First Name` = "Joe"
--     WHERE `Student Number` = 20230001


-- -- update last name
-- UPDATE member 
--     SET `Last Name` = "Goldberg"
--     WHERE `Student Number` = 20230001


-- -- update gender
-- UPDATE member 
--     SET `Gender` = "Nonbinary"
--     WHERE `Student Number` = 20230001


-- -- update degprog
-- UPDATE member 
--     SET `Degree Program` = "BS Psychology"
--     WHERE `Student Number` = 20230001


-- -- update batch
-- UPDATE member_batch 
--     SET `Batch` = "2015"
--     WHERE `Student Number` = 20230001
--         AND `Organization ID` = 11111111;