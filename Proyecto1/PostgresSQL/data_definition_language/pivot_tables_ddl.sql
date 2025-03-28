CREATE TABLE compras_temp (
    Fecha VARCHAR(16),
    CodProveedor VARCHAR(16),
    NombreProveedor VARCHAR(96),
    DireccionProveedor VARCHAR(256),
    NumeroProveedor VARCHAR(16),
    WebProveedor VARCHAR(16),
    CodProducto VARCHAR(24),
    NombreProducto VARCHAR(112),
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
COPY table_name (column1, column2, ...) FROM '/path/to/data.csv' DELIMITER ',' CSV;

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
    NombreProducto VARCHAR(112),
    MarcaProducto VARCHAR(24),
    Categoria VARCHAR(24),
    SodSucursal VARCHAR(16),
    NombreSucursal VARCHAR(24),
    DireccionSucursal VARCHAR(256),
    Region VARCHAR(24),
    Departamento VARCHAR(40),
    Unidades VARCHAR(16),
    PrecioUnitario VARCHAR(16)
);

drop table compras_temp
drop table ventas_temp


SELECT * FROM compras_temp

COPY compras_temp FROM '/home/SGFood02.comp' WITH  (FORMAT csv, HEADER true, DELIMITER '|')


