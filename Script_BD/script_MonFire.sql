CREATE DATABASE MonFire;
USE MonFire;

CREATE TABLE empresa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    razao_social VARCHAR(50) NOT NULL,
    cnpj CHAR(14) NOT NULL,
    dtHr DATETIME DEFAULT current_timestamp NOT NULL,
    nome_fantasia VARCHAR(50) NOT NULL
);
    
    CREATE TABLE usuario(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    fk_empresa INT NOT NULL, 
	CONSTRAINT empresa_usuario FOREIGN KEY (fk_empresa) REFERENCES empresa(id)
);
    
    CREATE TABLE maquina (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    dtHr DATETIME DEFAULT current_timestamp NOT NULL,
    fk_empresa INT NOT NULL,
    CONSTRAINT empresa_maquina FOREIGN KEY maquina(fk_empresa) REFERENCES empresa(id)
);
    
    CREATE TABLE componente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL, 
	dtHr DATETIME DEFAULT current_timestamp NOT NULL,
    fk_maquina INT NOT NULL,
    CONSTRAINT maquina_componente FOREIGN KEY componente(fk_maquina) REFERENCES maquina(id)
);

CREATE TABLE captura (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tipo VARCHAR(55),
    valor DOUBLE, 
    uni_medida CHAR(3),
    situacao VARCHAR(15),
    dtHr DATETIME DEFAULT current_timestamp NOT NULL, 
    fk_componente INT NOT NULL,
    CONSTRAINT componentes_captura FOREIGN KEY captura(fk_componente) REFERENCES componente(id),
    fk_maquina INT,
    CONSTRAINT maquina_captura FOREIGN KEY medicao(fk_maquina) REFERENCES maquina(id)
);
    
-- INSERTS:
insert into empresa (razao_social, cnpj, nome_fantasia) values
	('Monitoramento de Hardaware Bombeiro LTDA','01234567891234','MonFire'),
    ('Sptech Educacao Executiva e Servicos Ltda','26217610000135','São Paulo Tech School');
    
    
INSERT INTO maquina (nome, fk_empresa) VALUES 
	('Matheus Rocha', 2),
    ('Mickaela Rodrigues', 2),
    ('Raphael Oliveira', 2),
    ('Felipe Dias', 2),
    ('Enzo Valin', 2),
    ('Beatriz Sarro', 2);
    
INSERT INTO componente (nome, fk_maquina) VALUES 
	('CPU', 1),
    ('CPU', 2),
    ('CPU', 3),
    ('CPU', 4),
    ('CPU', 5),
    ('CPU', 6),
    ('RAM', 1),
    ('RAM', 2),
    ('RAM', 3),
    ('RAM', 4),
    ('RAM', 5),
    ('RAM', 6),
    ('DISCO', 1),
    ('DISCO', 2),
    ('DISCO', 3),
    ('DISCO', 4),
    ('DISCO', 5),
    ('DISCO', 6);

-- SELECT: 
SELECT c.id AS 'Número De Captura',
	m.nome AS 'Nome da Maquina', 
    tipo AS 'Tipo de Captura',
    comp.nome AS 'Nome Do Componentes',
	valor AS 'Valor Da Captura', 
    uni_medida AS 'Unidade De Medida',
    situacao AS 'Situação Da Captura',
	c.dtHr AS 'Data e Hora'
FROM captura as c JOIN maquina as m on fk_maquina = m.id JOIN componente AS comp ON comp.id = fk_componente;

select * from componente as c JOIN maquina AS m on c.fk_maquina = m.id;


create view ViewDisco as select nome, tipo, concat(valor, " " ,uni_medida) as valor, captura.dtHr from captura join componente on fk_componente = componente.id where nome ='DISCO' and tipo = 'Uso';
create view ViewCPU as select nome, tipo, concat(valor, " " ,uni_medida) as valor, captura.dtHr from captura join componente on fk_componente = componente.id where nome ='CPU' and tipo = 'Uso';
create view ViewRAM as select nome, tipo, concat(valor, " " ,uni_medida) as valor, captura.dtHr from captura join componente on fk_componente = componente.id where nome ='RAM' and tipo = 'Uso';

