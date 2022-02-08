-- Criando o Banco de Dados POIS (pontos de interesses)
-- Selecionando esse banco de dados
CREATE DATABASE POIS;
USE POIS;

-- Criando a tabela POI 
-- (INT - inteiro, NVARCHAR(100) - texto com no máximo 10 caracteres)
-- (NOT NULL - diferente de zero)
-- (IDENTITY - preenche de forma automática, sem o número inicial 1 e incrementando de 1 em 1)
-- (PRIMARY KEY - identificador exclusivo de um registro numa tabela)
-- (CHECK (X/Y >= 0) - checar se é maior ou igual a zero, ou seja, precisa ser positivo)
CREATE TABLE POI (
	ID INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
	NAME NVARCHAR(100) NOT NULL,
	X INT NOT NULL CHECK (X >= 0),
	Y INT NOT NULL CHECK (Y >= 0)
);

-- Inserido informação na tabela de forma manual (para testar)
INSERT INTO POI (NAME, X, Y) VALUES ('Lanchonete', 27, 12);

-- Selecionando a tabela criada (para testar)
SELECT * FROM POI;

-- Criando login, senha e usuário para integrar com o Banco de Dados
CREATE LOGIN SystemUser WITH PASSWORD = 'iDC%P#Nr6uLhLgnKKTuNJ72&aY5pwRWmoEoJ';
CREATE USER SystemUser FOR LOGIN SystemUser;
GRANT SELECT, INSERT ON POI TO SystemUser;

-- Checando o nome do servidor
SELECT @@SERVERNAME