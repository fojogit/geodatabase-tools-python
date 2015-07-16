enterprise geodatabase python tools
========================

The solution and project were setup using Visual Studio 2013 (Update 4) along with the [Python Tools for Visual Studio](http://pytools.codeplex.com/)


loaddata_sde_params/loaddata_sde_params.py
-------

### Summary: 
This is a sample python script that will load data from a specified directory to a specified enterprise geodatabase. The data location can be a directory that contains shapefiles or even a geodatabase. It uses geoprocessing tools and functions and can be run from ArcGIS Desktop, Engine, Server on Windows and Linux. 

### Name: 
loaddata_sde_params.py
### Description: 
Provide connection information to an Enterprise geodatabase and a data location. This will then load the data.

Type loaddata_sde_params.py -h or loaddata_sde_params.py --help for usage

Use at your own risk, but have fun too please. Enjoy.

### Examples:

(Linux)
/tmp>loaddata_sde_params.py --DBMS ORACLE -i myserver/orcl -u user1 -p user1 --dataloc /net/sharedata/location/data

(Windows)
c:\tmp>loaddata_sde_params.py --DBMS ORACLE -i myserver/orcl -u user1 -p user1 --dataloc \\sharedata\location\data

### FULL usage:

c:\>loaddata_sde_params.py --help

#### Usage: loaddata_sde_params.py [Options]

#### Options:
'''
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  --DBMS=DATABASE_TYPE  Type of enterprise DBMS: SQLSERVER, ORACLE, or
                        POSTGRESQL.
  -i INSTANCE           DBMS instance name
  --auth=ACCOUNT_AUTHENTICATION
                        Authentication type options (case-sensitive):
                        DATABASE_AUTH, OPERATING_SYSTEM_AUTH.
                        Default=DATABASE_AUTH
  -u USER               user name
  -p PASSWORD           password
  --dataloc=DATALOCATION
                        Path to the data (either a geodatabase or a directory
                        with shapefiles
  -D DATABASE           Database name (Not required for Oracle)

'''

### More Information on the tools used in this script:
[ArcGIS 10.1 help documentation](http://resources.arcgis.com/en/help/main/10.1/00qn/00qn0000001p000000.htm)

[ArcGIS FeatureClasstoGeodatabase Geoprocessing tool](http://resources.arcgis.com/en/help/main/10.1/index.html#/Feature_Class_To_Geodatabase/001200000021000000/)

[ArcGIS Upgrade Geodatabase (Data Management) Geoprocessing tool](http://resources.arcgis.com/en/help/main/10.1/0017/0017000000q7000000.htm)