-- QUERYS PREPARACIÓN DATABASE


-- Conectarse con usuario postgresql para crear el usuario tfgadmin y crear bvase de datos 
create database dogsorcats;
CREATE USER tfgadmin WITH PASSWORD 'tfgdatabase';
GRANT ALL PRIVILEGES ON DATABASE dogsorcats to tfgadmin;

psql -U tfgadmin -d dogsorcats -h 10.0.20.210 