"""
Name: loaddata_sde_params.py
Description: Provide connection information to an Enterprise geodatabase and a data location. This will then load the data.
Type loaddata_sde_params.py -h or loaddata_sde_params.py --help for usage
Use at your own risk, but have fun too please. Enjoy.

Examples:

(Linux)
/tmp>loaddata_sde_params.py --DBMS ORACLE -i myserver/orcl -u user1 -p user1 --dataloc /net/sharedata/location/data

(Windows)
c:\tmp>loaddata_sde_params.py --DBMS ORACLE -i myserver/orcl -u user1 -p user1 --dataloc \\sharedata\location\data

"""

# Import system modules

import arcpy, os, optparse, sys
from arcpy import env

# Define usage and version
parser = optparse.OptionParser(usage = "usage: %prog [Options]", version="%prog 2.0; valid for 10.1+ only")

#Define help and options
parser.add_option ("--DBMS", dest="Database_type", type="choice", choices=['SQLSERVER', 'ORACLE', 'POSTGRESQL', 'DB2','INFORMIX','DB2ZOS',''], default="", help="Type of enterprise DBMS: SQLSERVER, ORACLE, or POSTGRESQL.")
parser.add_option ("-i", dest="Instance", type="string", default="", help="DBMS instance name")
parser.add_option ("--auth", dest="account_authentication", type ="choice", choices=['DATABASE_AUTH', 'OPERATING_SYSTEM_AUTH'], default='DATABASE_AUTH', help="Authentication type options (case-sensitive):  DATABASE_AUTH, OPERATING_SYSTEM_AUTH.  Default=DATABASE_AUTH")
parser.add_option ("-u", dest="User", type="string", default="", help="user name")
parser.add_option ("-p", dest="Password", type="string", default="", help="password")
parser.add_option ("--dataloc", dest="DataLocation", type="string", default="", help="Path to the data (either a geodatabase or a directory with shapefiles")
parser.add_option ("-D", dest="Database", type="string", default="none", help="Database name (Not required for Oracle)")


def createDBConnectionFile(database_type, instance, database, username, password, account_authentication):
	if (database_type == ""):
		print "\nDatabase type must be specified!\n"
		parser.print_help()
		sys.exit(3)

	if (database_type == "SQLSERVER"):
		database_type = "SQL_SERVER"

	# Local variables
	instance_temp = instance.replace("\\","_")
	instance_temp = instance_temp.replace("/","_")
	instance_temp = instance_temp.replace(":","_")
	Conn_File_NameT = instance_temp + "_" + database + "_" + username

	if os.environ.get("TEMP") == None:
		temp = "c:\\temp"
	else:
		temp = os.environ.get("TEMP")

	if os.environ.get("TMP") == None:
		temp = "/usr/tmp"
	else:
		temp = os.environ.get("TMP")

	Connection_File_Name = Conn_File_NameT + ".sde"
	Connection_File_Name_full_path = temp + os.sep + Conn_File_NameT + ".sde"

	# Check for the .sde file and delete it if present
	arcpy.env.overwriteOutput=True
	if os.path.exists(Connection_File_Name_full_path):
		os.remove(Connection_File_Name_full_path)

	print "\nCreating Database Connection File...\n"
	# Process: Create Database Connection File...
	# Usage:  out_file_location, out_file_name, DBMS_TYPE, instance, database, account_authentication, username, password, save_username_password(must be true)
	outFile = arcpy.CreateDatabaseConnection_management(out_folder_path=temp, out_name=Connection_File_Name, database_platform=database_type, instance=instance, database=database, account_authentication=account_authentication, username=username, password=password, save_user_pass="TRUE")

	print Connection_File_Name_full_path
	arcpy.AddMessage("+++++++++\n")

	# Process: Checking the connection file created above
	try:
		# Execute ListUsers
		arcpy.ListUsers(outFile)
	except Exception, error:
		if "Connection information provided was for a non-administrative user" in str(error): # Connection was made as a non-admin, this is OK
			arcpy.AddMessage("Non-admin user.\n")
		else: # Connection was unsuccessful...
			arcpy.AddError(error)
			arcpy.AddMessage("\n+++++++++")
			arcpy.AddMessage("Exiting!!")
			arcpy.AddMessage("+++++++++\n")
			sys.exit(3)

		arcpy.AddMessage("Connection Successful!\n")
		arcpy.AddMessage("+++++++++\n")

	return Connection_File_Name_full_path

def main(argv):
        # Check if value entered for option
    try:
        (options, args) = parser.parse_args()

        #Check if no system arguments (options) entered
        if len(sys.argv) == 1:
            print "%s: error: %s\n" % (sys.argv[0], "No command options given")
            parser.print_help()
            sys.exit(3)

        #Usage parameters for spatial database connection
        account_authentication = options.account_authentication.upper()
        username = options.User.lower()
        password = options.Password
        dataloc = options.DataLocation
        database = options.Database.lower()
        database_type = options.Database_type.upper()
        instance = options.Instance

        # Get the current product license
        product_license=arcpy.ProductInfo()

        print "\n" + product_license + " license available!  Continuing..."
        arcpy.AddMessage("+++++++++")

        # Create the connection to the database and set the output location
        outLocation = createDBConnectionFile(database_type, instance, database, username, password, account_authentication)

        # Set environment settings
        # Set the workspace to the specified data location
        env.workspace = dataloc

        # Get all the feature classes in the environment
        # list of fc's should be similar to this: ["accident.shp", "veg.shp"]
        inFeatures = arcpy.ListFeatureClasses()

        # Process: Load Data (Use the "Feature Class To Geodatabase" Tool...)
        try:
            # Execute FeatureClassToGeodatabase
            print "Loading data...\n"
            arcpy.FeatureClassToGeodatabase_conversion(inFeatures, outLocation)

        except:
            for i in range(arcpy.GetMessageCount()):
                arcpy.AddReturnMessage(i)

        print "\nCleaning up..."
        arcpy.AddMessage("+++++++++")

        if os.path.exists(outLocation):
            os.remove(outLocation)

    #Check if no value entered for option
    except SystemExit as e:
        if e.code == 2:
            parser.usage = ""
            print "\n"
            parser.print_help()
            parser.exit(2)


if __name__ == "__main__":
    main(sys.argv)

