import mysql.connector
from settings import *

try:
    # Open the connection with the database
    connection = mysql.connector.connect(
        host=config("DbHost"),
        user=config("DbUsername"),
        port=config("DbPort"),
        passwd=config("DbPassword")
    )

except:
    print("Error occurred while trying to connect with the database. Check the credentials in the .env")
# Get a cursor
try:
    cursor = connection.cursor()
    connected = True
except:
    print("Cannot instantiate a cursor")

# Create Database and migrate tables
cursor.execute("CREATE DATABASE IF NOT EXISTS " + config("DbDatabase"))
cursor.execute("USE " + config("DbDatabase"))
# Create logs table
cursor.execute("CREATE TABLE IF NOT EXISTS  "+config("DbDatabase")+".`logs` ( `id` INT NOT NULL AUTO_INCREMENT , `event` VARCHAR(255) NOT NULL , `description` TEXT NULL DEFAULT NULL , `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`id`));")
# Create events table
cursor.execute("CREATE TABLE IF NOT EXISTS  "+config("DbDatabase")+".`events` ( `id` INT NOT NULL AUTO_INCREMENT , `video_folder` VARCHAR(255) NULL DEFAULT NULL , `filename` VARCHAR(255) NULL DEFAULT NULL , `camera` VARCHAR(255) NULL DEFAULT NULL , `model` VARCHAR(255) NULL DEFAULT NULL , `outcome` VARCHAR(255) NULL DEFAULT NULL , `object_label` VARCHAR(255) NULL DEFAULT NULL , `confidence` FLOAT NULL DEFAULT NULL , `payload` TEXT NULL DEFAULT NULL , `labels_found` TEXT NULL DEFAULT NULL , `total_frames` INT NULL DEFAULT NULL , `skipped_frames` INT NULL DEFAULT NULL , `frame` INT NULL DEFAULT NULL ,  `processor` VARCHAR(255) NULL DEFAULT NULL, `timestamp` TIMESTAMP NULL DEFAULT NULL , PRIMARY KEY (`id`));")
