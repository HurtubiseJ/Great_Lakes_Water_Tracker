USE [GreatLakesWaterLevels]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[SelectDateRange]
    @StationId NVARCHAR(30),
    @StartDate DATETIME, 
    @EndDate DATETIME
AS 
BEGIN 
    -- Validate input parameters
    IF @StationId IS NULL 
    BEGIN 
        RAISERROR('StationId cannot be NULL', 16, 1);
        RETURN;
    END

    IF @StartDate IS NULL 
    BEGIN 
        RAISERROR('StartDate cannot be null.', 16, 1);
        RETURN;
    END 

    IF @EndDate IS NULL 
    BEGIN 
        RAISERROR('EndDate cannot be NULL.', 16, 1);
        RETURN;
    END

    -- Retrieve the table name based on StationId
    DECLARE @TableName NVARCHAR(128);
    SET @TableName = (SELECT StationName FROM StationsId WHERE StationId = @StationId);

    -- Check if @TableName was found
    IF @TableName IS NULL
    BEGIN
        RAISERROR('No matching StationName found for the provided StationId.', 16, 1);
        RETURN;
    END

    -- Construct the SQL query without dynamic SQL
    DECLARE @SQL NVARCHAR(MAX);
    SET @SQL = 'SELECT * FROM ' + QUOTENAME(@TableName) + ' WHERE Date >= @StartDate AND Date <= @EndDate ORDER BY Date';

    -- Use EXEC instead of sp_executesql if the query does not require parameters
    EXEC sp_executesql @SQL, N'@StartDate DATETIME, @EndDate DATETIME', @StartDate, @EndDate;
END