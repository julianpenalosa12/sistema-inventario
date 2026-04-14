CREATE DATABASE inventario_db;

USE inventario_db;

CREATE TABLE usuarios(
  id_usuario INT auto_increment primary KEY,
  nombre varchar(100) not null,
  email  varchar(100) not null,
  password varchar(255) not null,
  rol varchar(50) not null,
  fecha_creacion timestamp default current_timestamp
);

create table categorias(
  id_categoria int auto_increment primary key,
  nombre varchar(100) not null,
  descripcion text
);

create table productos(
 id_producto int auto_increment primary key,
 nombre varchar(100) not null,
 descripcion text,
 precio decimal(10,2) not null,
 stock int not null,
 id_categoria int,
 foreign key (id_categoria) references categorias(id_categoria)
);

create table movimientos(
 id_movimiento int auto_increment primary key,
 id_producto int not null,
 tipo_movimiento ENUM('entrada','salida') not null,
 cantidad int not null,
 fecha timestamp default current_timestamp,
 id_usuario int,
 foreign key (id_producto) references productos(id_producto),
 foreign key (id_usuario) references usuarios(id_usuario)
);

create table logs(
 id_log int auto_increment primary key,
 accion varchar(255),
 fecha timestamp default current_timestamp,
 id_usuario int,
 foreign key (id_usuario) references usuarios(id_usuario)
);

select*from usuarios;

select*from categorias;

select*from movimientos;
insert into usuarios(nombre,email,password,rol)
values('Admin','admin@test.com','1234','admin')



