DROP TABLE Personas;
DROP TABLE Logros;

CREATE TABLE Personas (
PersonaID int PRIMARY KEY,
Apellido varchar(50) NOT NULL
);

CREATE TABLE Logros (
LogroID int PRIMARY KEY,
PersonaID int DEFAULT NULL,
Logro varchar(50) NOT NULL
);



INSERT INTO Personas (PersonaID,Apellido) VALUES (1,'Fleming');
INSERT INTO Personas (PersonaID,Apellido) VALUES (2,'Eratóstenes');
INSERT INTO Personas (PersonaID,Apellido) VALUES (3,'Newton');
INSERT INTO Personas (PersonaID,Apellido) VALUES (4,'Fernandez');

INSERT INTO Logros (LogroID,PersonaID,Logro) VALUES (1,1,'Descubrimiento de la Penicilina');
INSERT INTO Logros (LogroID,PersonaID,Logro) VALUES (2,2,'Cálculo del perímetro terrestre');
INSERT INTO Logros (LogroID,PersonaID,Logro) VALUES (3,3,'Ley de gravitación universal');
INSERT INTO Logros (LogroID,PersonaID,Logro) VALUES (4,3,'Desarrollo del Cálculo');
INSERT INTO Logros (LogroID,PersonaID,Logro) VALUES (5,NULL,'Cura del cancer');
