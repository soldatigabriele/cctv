import mysql.connector
from settings import *

try:
    # Open the connection with the database
    connection = mysql.connector.connect(
        host=config("Database.DbHost"),
        user=config("Database.DbUsername"),
        port=config("Database.DbPort"),
        passwd=config("Database.DbPassword"),
        auth_plugin='mysql_native_password'
    )
except:
    print("Error occurred while trying to connect with the database. Check the credentials in the .env")

with connection.cursor() as cursor:
    # Create Database and migrate tables
    cursor.execute("CREATE DATABASE IF NOT EXISTS " +
                config("Database.DbDatabase"))
    cursor.execute("USE " + config("Database.DbDatabase"))
    # Create logs table
    cursor.execute("CREATE TABLE IF NOT EXISTS  " + config("Database.DbDatabase") +
                ".`logs` ( `id` INT NOT NULL AUTO_INCREMENT , `event` VARCHAR(255) NOT NULL , `description` TEXT NULL DEFAULT NULL , `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , PRIMARY KEY (`id`));")
    # Create events table
    cursor.execute("CREATE TABLE IF NOT EXISTS  " + config("Database.DbDatabase") + ".`events` ( `id` INT NOT NULL AUTO_INCREMENT , `video_folder` VARCHAR(255) NULL DEFAULT NULL , `filename` VARCHAR(255) NULL DEFAULT NULL , `camera` VARCHAR(255) NULL DEFAULT NULL , `model` VARCHAR(255) NULL DEFAULT NULL , `outcome` VARCHAR(255) NULL DEFAULT NULL , `object_label` VARCHAR(255) NULL DEFAULT NULL , `confidence` FLOAT NULL DEFAULT NULL , `payload` TEXT NULL DEFAULT NULL , `labels_found` TEXT NULL DEFAULT NULL , `total_frames` INT NULL DEFAULT NULL , `skipped_frames` INT NULL DEFAULT NULL , `frame` INT NULL DEFAULT NULL ,  `processor` VARCHAR(255) NULL DEFAULT NULL, `timestamp` TIMESTAMP NULL DEFAULT NULL , PRIMARY KEY (`id`));")
    # Create messages table
    cursor.execute("CREATE TABLE IF NOT EXISTS  " + config("Database.DbDatabase") +
                ".`messages` ( `id` INT NOT NULL AUTO_INCREMENT , `chat_id` VARCHAR(255), `message_id` VARCHAR(255), `timestamp` TIMESTAMP NULL DEFAULT NULL , PRIMARY KEY (`id`));")

print("migration succesful")
