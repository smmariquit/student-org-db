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

-- questions - should we keep text fields to a standard 255 or better to adjust based on their capability?
-- notes:
-- Role and status is actually a reserver keyword in SQL
-- When a PRIMARY KEY constraint is added, it is automatically UNIQUE

-- CONSTRAINT UK_Joins UNIQUE KEY (StudentNumber, OrganizationId, AcademicYear, Semester)
-- This means that UNIQUE KEY constraint, named UK_Joins, means that the combination of the values in the StudentNumber, OrganizationId, AcademicYear, and Semester columns must be unique across all rows in the table. It does not mean that each individual attribute (StudentNumber, OrganizationId, AcademicYear, Semester) must be unique on its own. Same goes sa primary key
-- An attribute that was put in the primary key constraint cannot be separately put in a unique key constraint

-- Elliott Arthur Walleck
-- Mary Lamont Milburn
-- Billy Dudley Tegenkamp
-- Nathaniel Arthur Tegenkamp
-- Clement Malcolm Alhameed
-- Nathaniel Malcolm Strowbridge
-- Elliott Dudley Tegenkamp
-- Clement Deangelo Alhameed

-- CREATE STATEMENTS

CREATE USER organizationer IDENTIFIED BY ('uplbsqlsociety');

CREATE DATABASE organization;

GRANT CREATE, UPDATE, DROP, DELETE, INSERT, SELECT ON organization.* TO 'organizationer'@'localhost';

CREATE TABLE Organization (
    OrganizationId int NOT NULL,
    OrganizationName varchar(255),
    CONSTRAINT PK_Organization PRIMARY KEY (OrganizationId)
);

CREATE TABLE Member (
    StudentNumber varchar(255) NOT NULL,
    FirstName varchar(255) NOT NULL,
    MiddleName varchar(255), -- some ppl have no middle name
    LastName varchar(255) NOT NULL,
    Gender varchar(255), 
    DegreeProgram varchar(255),
    CONSTRAINT PK_Member PRIMARY KEY (StudentNumber)
);

CREATE TABLE Joins (
    StudentNumber varchar(255) NOT NULL ,
    OrganizationId varchar(255) NOT NULL,
    AcademicYear varchar(255) NOT NULL,
    Semester varchar(255) NOT NULL,
    MemberRole varchar(255) NOT NULL,
    MemberStatus varchar(255) NOT NULL
    CONSTRAINT PK_Joins PRIMARY KEY (StudentNumber, OrganizationId, AcademicYear, Semester)
    CONSTRAINT UQ_SN UNIQUE (StudentNumber) -- wait what if hindi nag eexist yung S/N sa Member table? wala bang constraint for that? why wouldnt it exist there lahat naman ng member may std no
);

CREATE TABLE MemberBatch (
    StudentNumber varchar(255) NOT NULL,
    OrganizationId varchar(255) NOT NULL,
);


-- 1. View all members of the organization by role, status, gender, degree program, batch (year of membership), and committee. (Note: we assume one committee membership only per organization per semester) 

CREATE OR REPLACE VIEW membersvu(student_number, last_name, first_name, role, status, gender, degree_program, batch, committee)
    AS SELECT m.StudentNumber, m.LastName, m.FirstName, 
    sr.Role, j.Status, m.Gender, m.DegreeProgram, 
    mb.Batch, sr.CommitteeName
    FROM Member m
    JOIN MemberBatch mb on m.StudentNumber = mb.StudentNumber 
    JOIN StudentRole sr on mb.StudentNumber = sr.StudentNumber
    JOIN Joins j ON m.StudentNumber = j.StudentNumber
        AND mb.OrganizationId = j.OrganizationId
    WHERE sr.OrganizationId = "givenOrganization"  


-- 2. View members for a given organization with unpaid membership fees or dues for a given semester and academic year. 
CREATE OR REPLACE VIEW unpaid_fees_orgvu(student_number, last_name, first_name, fee_name, amount, due_date) 
    AS SELECT m.StudentNumber, m.LastName, m.FirstName, f.FeeName, f.Amount, f.DueDate
    FROM Member m 
    JOIN Fee f ON m.StudentNumber = f.StudentNumber 
    WHERE f.Status = 'unpaid' 
    AND f.OrganizationId = 'givenOrganization'
    AND f.AcademicYear = 'givenAcademicYear'
    AND f.Semester = 'givenSemester';



-- 3. View a member's unpaid membership fees or dues for all their organizations (Member's POV). 
CREATE OR REPLACE VIEW unpaid_fees_membervu(organization_id, fee_name, amount, due_date, academic_year, semester)
    AS SELECT f.OrganizationId, f.FeeName, f.Amount, f.DueDate, f.AcademicYear, f.Semester
    FROM Fee f
    WHERE f.Status = 'unpaid';


-- 4. View all executive committee members of a given organization for a given academic year. 

CREATE OR REPLACE VIEW executive_comittee_membersvu(student_number, last_name, first_name, committee_name, semester)
    AS SELECT m.StudentNumber, m.LastName, m.FirstName, sr.CommitteeName, c.Semester
    FROM Member m
    JOIN StudentRole sr ON m.StudentNumber = sr.StudentNumber
    JOIN Committee c ON sr.CommitteeName = c.CommitteeName
        AND sr.OrganizationId = c.OrganizationId
    WHERE sr.OrganizationId = 'givenOrganization'
    AND c.AcademicYear = 'givenAcademicYear'
    AND c.CommitteeName = 'Executive';


-- 5. View all Presidents (or any other role) of a given organization for every academic year in reverse chronological order (current to past).

CREATE OR REPLACE VIEW organization_rolevu(student_number, last_name, first_name, academic_year)
    AS SELECT m.StudentNumber, m.LastName, m.FirstName, j.AcademicYear
    FROM Member m
    JOIN Joins j ON m.StudentNumber = j.StudentNumber
    WHERE j.Role = 'givenRole'
        AND j.OrganizationId = 'givenOrgId'
-- ordering should be in view query (https://stackoverflow.com/questions/15187676/create-a-view-with-order-by-clause)


-- 6. View all late payments made by all members of a given organization for a given semester and academic year. 
-- 7. View the percentage of active vs inactive members of a given organization for the last n semesters. (Note: n is a positive integer) 
-- 8. View all alumni members of a given organization as of a given date. 
-- 9. View the total amount of unpaid and paid fees or dues of a given organization as of a given 
-- date. 
-- 10. View the member/s with the highest debt of a given organization for a given semester. 

