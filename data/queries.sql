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
    CONSTRAINT UQ_SN UNIQUE (StudentNumber) -- wait what if hindi nag eexist yung S/N sa Member table? wala bang constraint for that?
);

CREATE TABLE MemberBatch (
    StudentNumber varchar(255) NOT NULL,
    OrganizationId varchar(255) NOT NULL,
);