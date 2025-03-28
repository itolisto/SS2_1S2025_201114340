CREATE DATABASE pivot_tables;
GO

USE pivot_tables;
GO

CREATE TABLE compras_temp (
    Fecha VARCHAR(16),
    CodProveedor VARCHAR(16),
    NombreProveedor VARCHAR(96),
    DireccionProveedor VARCHAR(256),
    NumeroProveedor VARCHAR(16),
    WebProveedor VARCHAR(16),
    CodProducto VARCHAR(24),
    NombreProducto VARCHAR(96),
    MarcaProducto VARCHAR(32),
    Categoria VARCHAR(48),
    SodSucursal VARCHAR(16),
    NombreSucursal VARCHAR(48),
    DireccionSucursal VARCHAR(256),
    Region VARCHAR(24),
    Departamento VARCHAR(40),
    Unidades VARCHAR(16),
    CostoU VARCHAR(16)
);
GO

CREATE TABLE ventas_temp (
    Fecha VARCHAR(16),
    CodigoCliente VARCHAR(16),
    NombreCliente VARCHAR(96),
    TipoCliente VARCHAR(24),
    DireccionCliente VARCHAR(128),
    NumeroCliente VARCHAR(16),
    CodVendedor VARCHAR(16),
    NombreVendedor VARCHAR(48),
    Vacacionista VARCHAR(8),
    CodProducto VARCHAR(32),
    NombreProducto VARCHAR(88),
    MarcaProducto VARCHAR(24),
    Categoria VARCHAR(24),
    SodSucursal VARCHAR(16),
    NombreSucursal VARCHAR(24),
    DireccionSucursal VARCHAR(96),
    Region VARCHAR(24),
    Departamento VARCHAR(40),
    Unidades VARCHAR(16),
    PrecioUnitario VARCHAR(16)
);
GO

DROP TABLE dbo.compras_temp
DROP TABLE dbo.ventas_temp

TRUNCATE TABLE dbo.ventas_temp
GO

DELETE FROM dbo.ventas_temp

BULK INSERT dbo.compras_temp
FROM '/home/SGFood01.comp'
WITH (
  FIELDTERMINATOR = '|', 
  ROWTERMINATOR = '0x0a',
  FIRSTROW = 2
)

TRUNCATE TABLE dbo.ventas_temp
GO

SELECT * FROM dbo.ventas_temp

BULK INSERT dbo.ventas_temp
FROM '/home/SGFood01.vent'
WITH (
  FIELDTERMINATOR = '|', 
  ROWTERMINATOR = '0x0a',
  FIRSTROW = 2
)