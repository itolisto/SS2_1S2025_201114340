USE master
GO

DROP DATABASE IF EXISTS seminario
GO

CREATE DATABASE seminario
GO

USE seminario
GO

DROP SCHEMA IF EXISTS project1
GO

CREATE SCHEMA project1
GO

IF OBJECT_ID('project1.fact_compras', 'U') IS NOT NULL
    DROP TABLE project1.fact_compras;
GO

IF OBJECT_ID('project1.pivot_fact_compras', 'U') IS NOT NULL
    DROP TABLE project1.pivot_fact_compras;
GO

IF OBJECT_ID('project1.dim_proveedor', 'U') IS NOT NULL
    DROP TABLE project1.dim_proveedor;
GO

IF OBJECT_ID('project1.dim_fecha', 'U') IS NOT NULL
    DROP TABLE project1.dim_fecha;
GO

IF OBJECT_ID('project1.dim_sucursal', 'U') IS NOT NULL
    DROP TABLE project1.dim_sucursal;
GO

IF OBJECT_ID('project1.dim_producto', 'U') IS NOT NULL
    DROP TABLE project1.dim_producto;
GO

IF OBJECT_ID('project1.dim_marca', 'U') IS NOT NULL
    DROP TABLE project1.dim_marca;
GO

IF OBJECT_ID('project1.dim_categoria', 'U') IS NOT NULL
    DROP TABLE project1.dim_categoria;
GO

IF OBJECT_ID('project1.fact_ventas', 'U') IS NOT NULL
    DROP TABLE project1.fact_ventas;
GO

IF OBJECT_ID('project1.pivot_fact_ventas', 'U') IS NOT NULL
    DROP TABLE project1.pivot_fact_ventas;
GO

IF OBJECT_ID('project1.dim_cliente', 'U') IS NOT NULL
    DROP TABLE project1.dim_flight_status;
GO

IF OBJECT_ID('project1.dim_tipo_cliente', 'U') IS NOT NULL
    DROP TABLE project1.dim_tipo_cliente;
GO

IF OBJECT_ID('project1.dim_vendedor', 'U') IS NOT NULL
    DROP TABLE project1.dim_vendedor;
GO


CREATE TABLE project1.[fact_compras] (
	[id] INTEGER NOT NULL IDENTITY UNIQUE,
	[sk_proveedor_id] INTEGER NOT NULL,
	[sk_categoria_prod] INTEGER NOT NULL,
	[sk_marca_prod] INTEGER NOT NULL,
	[sk_fecha] INTEGER NOT NULL,
	[sk_sucursal] INTEGER NOT NULL,
	[sk_producto] INTEGER NOT NULL,
	[costo_unitario] DECIMAL(18, 2) NOT NULL,
	[unidades] INTEGER NOT NULL,
	PRIMARY KEY([id])
);
GO

CREATE TABLE project1.[dim_proveedor] (
	[id_codigo] INTEGER NOT NULL,
	[nombre] NVARCHAR(192) NOT NULL,
	[direccion] NVARCHAR(256) NOT NULL,
	[numero] INTEGER NOT NULL,
	[web] CHAR(4) NOT NULL,
	PRIMARY KEY([id_codigo])
);
GO

CREATE TABLE project1.[dim_fecha] (
	[id] INTEGER NOT NULL UNIQUE,
	[dia] SMALLINT NOT NULL,
	[mes] TINYINT NOT NULL,
	[anio] SMALLINT NOT NULL,
	[fecha] DATE NOT NULL,
	PRIMARY KEY([id])
);
GO

CREATE INDEX [dim_fecha_index_0]
ON project1.[dim_fecha] ([anio]);
GO

CREATE TABLE project1.[dim_sucursal] (
	[id_codigo] INTEGER NOT NULL UNIQUE,
	[nombre] VARCHAR(48) NOT NULL,
	[direccion] NVARCHAR(256) NOT NULL,
	[region] VARCHAR(24) NOT NULL,
	[departamento] VARCHAR(40) NOT NULL,
	PRIMARY KEY([id_codigo])
);
GO

CREATE TABLE project1.[dim_producto] (
	[id] INTEGER IDENTITY NOT NULL,
	[codigo] VARCHAR(24) NOT NULL UNIQUE,
	[nombre] NVARCHAR(256) NOT NULL,
	PRIMARY KEY([id])
);
GO

CREATE TABLE project1.[dim_marca] (
	[id] INTEGER NOT NULL IDENTITY UNIQUE,
	[nombre] VARCHAR(32) NOT NULL UNIQUE,
	PRIMARY KEY([id])
);
GO

CREATE TABLE project1.[dim_categoria] (
	[id] INTEGER NOT NULL IDENTITY UNIQUE,
	[nombre] NVARCHAR(96) NOT NULL,
	PRIMARY KEY([id])
);
GO


CREATE TABLE project1.[fact_ventas] (
	[id] INTEGER NOT NULL IDENTITY UNIQUE,
	[sk_categoria_prod] INTEGER NOT NULL,
	[sk_marca_prod] INTEGER NOT NULL,
	[sk_producto] INTEGER NOT NULL,
	[sk_sucursal] INTEGER NOT NULL,
	[sk_fecha] INTEGER NOT NULL,
	[sk_vendedor] INTEGER NOT NULL,
	[sk_cliente] INTEGER NOT NULL,
	[sk_tipo_cliente] INTEGER NOT NULL,
	[precio_unitario] DECIMAL(18, 2) NOT NULL,
	[unidades] INTEGER NOT NULL,
	PRIMARY KEY([id])
);
GO

CREATE TABLE project1.[pivot_fact_compras] (
	[id] INTEGER NOT NULL IDENTITY UNIQUE,
	[categoria_prod] NVARCHAR(96) NOT NULL,
	[marca_prod] VARCHAR(32) NOT NULL,
	[cod_producto] VARCHAR(24) NOT NULL,
	[sucursal] INTEGER NOT NULL,
	[fecha] INTEGER NOT NULL,
	[nombre_proveedor] NVARCHAR(192) NOT NULL,
	[costo_unitario] DECIMAL(18, 2) NOT NULL,
	[unidades] INTEGER NOT NULL
);

CREATE TABLE project1.[pivot_fact_ventas] (
	[id] INTEGER NOT NULL IDENTITY UNIQUE,
	[categoria_prod] NVARCHAR(96) NOT NULL,
	[marca_prod] VARCHAR(32) NOT NULL,
	[cod_producto] VARCHAR(24) NOT NULL,
	[sucursal] INTEGER NOT NULL,
	[fecha] INTEGER NOT NULL,
	[vendedor] INTEGER NOT NULL,
	[nombre_vendedor] NVARCHAR(96) NOT NULL,
	[tipo_vendedor] VARCHAR(16),
	[cliente] INTEGER NOT NULL,
	[tipo_cliente] CHAR(8) NOT NULL,
	[precio_unitario] DECIMAL(18, 2) NOT NULL,
	[unidades] INTEGER NOT NULL
);
GO

CREATE TABLE project1.[dim_cliente] (
	[id_codigo] INTEGER NOT NULL UNIQUE,
	[nombre] NVARCHAR(192) NOT NULL,
	[direccion] NVARCHAR(256) NOT NULL,
	[numero] INTEGER NOT NULL,
	PRIMARY KEY([id_codigo])
);
GO

CREATE TABLE project1.[dim_tipo_cliente] (
	[id] INTEGER NOT NULL IDENTITY UNIQUE,
	[tipo] CHAR(8) NOT NULL,
	PRIMARY KEY([id])
);
GO

CREATE TABLE project1.[dim_vendedor] (
	[id] INTEGER NOT NULL IDENTITY,
	[id_codigo] INTEGER NOT NULL,
	[Nombre] NVARCHAR(96) NOT NULL,
	[tipo] VARCHAR(16) NOT NULL,
	PRIMARY KEY([id])
);
GO

select * from project1.fact_ventas
select * from project1.pivot_fact_ventas

select * from project1.dim_categoria

select * from project1.dim_proveedor

select * from project1.dim_marca

delete from project1.pivot_fact_compras
delete from project1.pivot_fact_ventas


select * from project1.dim_categoria ff
left join project1.pivot_fact_compras cc on ff.nombre = 'charcutería'
where cc.categoria_prod = 'charcutería'

select * from project1.pivot_fact_ventas
where categoria_prod = 'charcutería' 
and marca_prod = 'monticello' 
and cod_producto = 'AC00003' 
and sucursal = 1 
and fecha = 20200114 
and vendedor = 1 
and nombre_vendedor = 'nelson mario caffera morandi'
and tipo_vendedor = 'fijo'
and cliente = 1
and tipo_cliente = 'min'
and precio_unitario = 398.27
and unidades = 34

select * from project1.pivot_fact_ventas where id = 1
select * from project1.pivot_fact_compras where id = 1

CREATE INDEX [dim_vendedor_index_0]
ON project1.[dim_vendedor] ([id_codigo]);
GO

ALTER TABLE project1.[fact_compras]
ADD FOREIGN KEY([sk_proveedor_id]) REFERENCES project1.[dim_proveedor]([id_codigo])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_compras]
ADD FOREIGN KEY([sk_categoria_prod]) REFERENCES project1.[dim_categoria]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_compras]
ADD FOREIGN KEY([sk_marca_prod]) REFERENCES project1.[dim_marca]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_compras]
ADD FOREIGN KEY([sk_producto]) REFERENCES project1.[dim_producto]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_compras]
ADD FOREIGN KEY([sk_sucursal]) REFERENCES project1.[dim_sucursal]([id_codigo])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_compras]
ADD FOREIGN KEY([sk_fecha]) REFERENCES project1.[dim_fecha]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_categoria_prod]) REFERENCES project1.[dim_categoria]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_marca_prod]) REFERENCES project1.[dim_marca]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_producto]) REFERENCES project1.[dim_producto]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_sucursal]) REFERENCES project1.[dim_sucursal]([id_codigo])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_fecha]) REFERENCES project1.[dim_fecha]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_vendedor]) REFERENCES project1.[dim_vendedor]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_tipo_cliente]) REFERENCES project1.[dim_tipo_cliente]([id])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO

ALTER TABLE project1.[fact_ventas]
ADD FOREIGN KEY([sk_cliente]) REFERENCES project1.[dim_cliente]([id_codigo])
ON UPDATE NO ACTION ON DELETE NO ACTION;
GO
