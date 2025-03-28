docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=abcdeF1+" \
-p 1433:1433 --name sql1 --hostname sql1 \
-d \
-v 'C:\Users\Juan Enrique\seminario2\lab\project1\ArchivosdeentradaProyecto':/usr:rw \
mcr.microsoft.com/mssql/server:2022-latest
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "abcdeF1+" -No

Postgres automatically creates 'postgres' db if the user defines another like in the below commands this default db will be actually have nothing and no privileges 

docker run --name seminario_postrgres \
	-e POSTGRES_USER=edgar \   # if not set default value will be used, "postgres"
	-e POSTGRES_PASSWORD=1234567A \
	-e POSTGRES_DB=edgar \ # if not set value will be the same as "POSTGRES_USER"
	-p 5432:5432 \
	-v 'C:\Users\Juan Enrique\seminario2\lab\project1\ArchivosdeentradaProyecto':/home:rw \
	-d postgres

download postgres odbc(setup.exe)

https://www.postgresql.org/ftp/odbc/releases/REL-17_00_0004-mimalloc/

List databases
```
SELECT datname FROM pg_database
WHERE datistemplate = false;
```

Other option is to start psql in container command line, login to user
```
pslq -U edgar -W 1234567A
```

run this command
```
\l
```

In order to use an specific database from any connection make sure you specify the database you want to work with in that connection, this means you can not swith with SQL commands to another database when running form a db manager like DBeaver, you can only select the db when connecting to postgres


Download PostgreSQL and only install `command line tools`
https://www.postgresql.org/download/windows/

This tool only helped me understand what was wrong with the query, it turns out that when doing this `COPY` command, if you execute it from "dbbeaver" or "pgdmin" it will not complain about enconding but if I execute it from SSIS or using the "psql" command line tool I installed in previous step I will get an error, in SSIS because it is doesn't work great with these type of connections I will get an error and the "result set" won't know how to parse it but if I "debug" trying to execute same command using from command line with this command `export PGPASsWORD=1234567A && psql.exe -h localhost -p 5432 -d edgar -U edgar -c "COPY compras_temp FROM '/home/SGFood02.comp' WITH  (FORMAT text, HEADER true, DELIMITER '|');"` I will then get more info about what went wrong, in this case is some Spanish characters(tilde) which can not be encode/decode because encoding is not configured to work  with these type of characters, so after investigating I found the most easy and simple way to specify a proper encoding standard
```
# works in db managers but not in git bash or command line in windows
COPY compras_temp FROM '/home/SGFood02.comp' WITH  (FORMAT text, HEADER true, DELIMITER '|');

# works everywhere
COPY compras_temp FROM '/home/SGFood02.comp' WITH  (FORMAT text, HEADER true, DELIMITER '|', ENCODING 'UTF8');
```

Funny thing is that if I add this `export PGPASsWORD=1234567A && psql.exe -h localhost -p 5432 -d edgar -U edgar -c "COPY compras_temp FROM '/home/SGFood02.comp' WITH  (FORMAT text, HEADER true, DELIMITER '|');" > error.txt` it will encode the file correctly, and this gives me other option inside my SSIS project, I could store this in a bash script and use a "Execute Process task", the advantage of using this process is that we can get a log more easily

# Inserting Unicode characters to sql server
At first I was using this command
```
BULK INSERT dbo.compras_temp
FROM '/home/SGFood01.comp'
WITH (
  FIELDTERMINATOR = '|', 
  ROWTERMINATOR = '0x0a',
  FIRSTROW = 2,
)
```

But then realized Spanish "tildes" where not being parsed correctly, after some search I found this command
```
BULK INSERT dbo.compras_temp
FROM '/home/SGFood01.comp'
WITH (
  FIELDTERMINATOR = '|', 
  ROWTERMINATOR = '0x0a',
  FIRSTROW = 2,
  CODEPAGE = '65001'
)
```

Code page "65001" is basically "UTF-8" but in linux SQL server doesn't support this feature yet(my docker desktop container is running using linux) so after investigating I found that UTF-16 is supported and that way I can insert Unicode characters. I had to parse the original file but first, using git bash in Windows, I check file info
```
file SGFood01.comp
```

If it is using UTF-8 I can run the following command using the bash utility `iconv` to parse it to UTF-16
```
echo -ne '\xFF\xFE' > SGFood01-16.comp   # this is the EOF character
iconv -f UTF-8 -t UTF-16LE SGFood01.comp >> SGFood01-16.comp
```

And now the insert command will change to
```
BULK INSERT dbo.compras_temp
FROM '/home/SGFood01-16.comp'
WITH (
  DATAFILETYPE = 'widechar',
  FIELDTERMINATOR = '|', 
  ROWTERMINATOR = '\n',
  FIRSTROW = 2
)
```

Repeat same process with sales(ventas) file

# Transformations

## Compras
1. En el "codigo de proveedor" removere espacios vacios al inico y final. Los nulos y vacios se sustituiran con el valor por defecto "0000", para poder utilizar este valor como llave primaria numerica se removera la primera letra del codigo

2. El "nombre de proveedor" todos sus caracteres estaran en minusculas y removere comillas simples y dobles, espacios vacios al inicio y al final, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes) 

3. La "direccion de proveedor" tendra caracteres en minusculas y removere comillas simples y dobles, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes)

4. En el "numero de proveedor" removere cualquier caracter(en caso de error) y si el valor es nulo o diferente a un numero entonces pondre ceros	

5. El "codigo de producto" se sustituiran vacios y nulos con el valor por defecto "PR00000"

6. El "nombre de producto" removere espacios vacios al inico y final y todo sera minusculas(tentativamente se quitaran tildes)

7. En la "marca de producto" removere espacios vacios al incio y final, valores nulos y vacios seran por defecto "sin marca" y todo sera minusculas(tentativamente se quitaran tildes)

8. En la "categoria" removere espacios vacios al incio y final, valores nulos y vacios seran por defecto "sin categoria" y todo sera minusculas(tentativamente se quitaran tildes)

9. En el "codigo de sucursal" removere la primera letra y dejare solo los numeros para usarlo como un primary key

10. En la "direccion sucursal" removere espacios vacios al incio y final, tambien comillas simples y dobles. Valores nulos y vacios seran por defecto "sin direccion" y todo sera minusculas(tentativamente se quitaran tildes)
 
11. En la "region" removere espacios vacios al incio y final, valores nulos y vacios seran por defecto "sin region" y todo sera minusculas(tentativamente se quitaran tildes)

12. En el "departamento" removere espacios vacios al incio y final, valores nulos y vacios seran por defecto "sin departamento" y todo sera minusculas(tentativamente se quitaran tildes)

## Ventas

1. En el "codigo de cliente" removere espacios vacios al inico y final, los nulos y vacios para standarizar los datos, para los nulos y los vacios el valor por defecto sera "0000", ademas para poder usar este valor como llave primaria removere la letra inicial

2. En el "nombre de cliente" todos sus caracteres estaran en minusculas y removere espacios vacios al inicio y al final, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes)

3. El "tipo de cliente" sera asignado "min" para Minorista y "may" para Mayorista

4. La "direccion de cliente" tendra caracteres en minusculas y removere comillas simples y dobles, espacios vacios al inicio y final, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes)

5. En el "numero de cliente" removere espacios vacios al inicio y al final y nulos y si el valor es nulo o diferente a un numero entonces pondre cero

6. En el "nombre vendedor" volvere todas las letras minuscula(tentativamente se quitaran tildes)

7. En el "codigo vendedor" quitare espacios en blanco al inicio y al final, y removere la primera letra para poder usar el valor como numerio en una llave primaria y los valores vacios o nulos tendran por defecto "0000"

7. En "vacacionista" se sustituira 1 por "vacacionista" y cualquier 1 por "fijo", nulos y vacios seran "indefinido" esto nos cubrira los nulos y valores no validos y esto se insertara en una columna nueva llamada "TipoVendedor", este cambio se hace con la mejorar la legibilidad del analisis

8. En el "nombre de producto" todos sus caracteres estaran en minusculas y removere espacios vacios al inicio y al final, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes)

9. En la "marca producto" todos sus caracteres estaran en minusculas y removere espacios vacios al inicio y al final, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes)

10. En la "categoria" todos sus caracteres estaran en minusculas y removere espacios vacios al inicio y al final, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes)

11. En el "codigo de sucursal" removere la primera letra y dejare solo los numeros para usar los como un primary key

12. En la "direccion sucursal" todos sus caracteres estaran en minusculas y removere espacios vacios al inicio y al final, comillas simples y dobles, para estandarizar minusculas en todo el data warehouse(tentativamente se quitaran tildes)

13. En la "region" removere espacios vacios al incio y final, valores nulos y vacios seran por defecto "sin region" y todo sera minusculas(tentativamente se quitaran tildes)

14. En el "departamento" removere espacios vacios al incio y final, valores nulos y vacios seran por defecto "sin departamento" y todo sera minusculas(tentativamente se quitaran tildes)


669

357
