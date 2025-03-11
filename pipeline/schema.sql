-- This file should contain all code required to create & seed database tables.

-- DROP DATABASE IF EXISTS museum;
-- CREATE DATABASE museum;
-- \c museum;


DROP TABLE IF EXISTS request_interaction;
DROP TABLE IF EXISTS rating_interaction;
DROP TABLE IF EXISTS exhibition;
DROP TABLE IF EXISTS request;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS floor;
DROP TABLE IF EXISTS department;



CREATE TABLE department (
    department_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    department_name VARCHAR(100) NOT NULL
);

CREATE TABLE floor (
    floor_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    floor_name VARCHAR(100) NOT NULL
);


CREATE TABLE request (
    request_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    request_value INT CHECK (request_value in (0, 1)),
    request_description VARCHAR(10) CHECK (LOWER(request_description) in ('assistance', 'emergency'))
);

CREATE TABLE rating (
    rating_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    rating_value INT CHECK (rating_value in (0, 1, 2, 3, 4)),
    rating_description VARCHAR(8) CHECK (LOWER(rating_description) in ('terrible', 'bad', 'neutral', 'good', 'amazing'))
);

CREATE TABLE exhibition (
    exhibition_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    exhibition_name VARCHAR(100) NOT NULL,
    exhibition_description VARCHAR(100),
    department_id INT NOT NULL, --foreign key to department
    floor_id INT NOT NULL, --foreign key to floor
    exhibition_start_date DATE NOT NULL, 
    public_id CHAR(6),
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (floor_id) REFERENCES floor(floor_id)
);


CREATE TABLE request_interaction (
    request_interaction_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    exhibition_id INT NOT NULL, --foreign key to exhibition
    request_id INT NOT NULL, --foreign key to request
    event_at TIMESTAMPTZ NOT NULL, 
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (request_id) REFERENCES request(request_id)
);


CREATE TABLE rating_interaction (
    rating_interaction_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    exhibition_id INT NOT NULL, --foreign key to exhibition
    rating_id INT NOT NULL, --foreign key to rating
    event_at TIMESTAMPTZ,
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id)
);



CREATE INDEX exhibition_department_idx ON exhibition (department_id);
CREATE INDEX exhibition_floor_idx ON exhibition (floor_id);
CREATE INDEX exhibition_start_date_idx ON exhibition (exhibition_start_date);
CREATE INDEX request_value_idx ON request (request_value);
CREATE INDEX rating_value_idx ON rating (rating_value);



INSERT INTO rating (rating_value, rating_description)
VALUES 
(0, 'Terrible'),
(1, 'Bad'),
(2, 'Neutral'),
(3, 'Good'),
(4, 'Amazing');

INSERT INTO request (request_value, request_description)
VALUES 
(0, 'assistance'),
(1, 'emergency');


INSERT INTO department (department_name)
VALUES 
('Entomology'),
('Geology'),
('Paleontology'),
('Zoology'),
('Ecology');

INSERT INTO floor (floor_name)
VALUES 
('Vault'),
('1'),
('2'),
('3');


INSERT INTO exhibition (
    exhibition_name,
    exhibition_description,
    department_id, --foreign key to department
    floor_id, --foreign key to floor
    exhibition_start_date, 
    public_id)
VALUES 
('Adaptation', 'How insect evolution has kept pace with an industrialised world', 1, 4, TO_DATE('01/07/19', 'DD/MM/YY'), 'EXH_01'),
('Measureless to Man', 'An immersive 3D experience: delve deep into a previously-inaccessible cave system.', 2, 1, TO_DATE('23/08/21', 'DD/MM/YY'), 'EXH_00'),
('Thunder Lizards', 'How new research is making scientists rethink what dinosaurs really looked like.', 3, 1, TO_DATE('01/02/23', 'DD/MM/YY'), 'EXH_05'),
('The Crenshaw Collection', 'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.', 4, 2, TO_DATE('03/03/21', 'DD/MM/YY'), 'EXH_02'),
('Our Polluted World', 'A hard-hitting exploration of humanity"s impact on the environment.', 5, 3, TO_DATE('12/05/21', 'DD/MM/YY'), 'EXH_04'),
('Cetacean Sensations', 'Whales: from ancient myth to critically endangered.', 4, 1, TO_DATE('01/07/19', 'DD/MM/YY'), 'EXH_03');

