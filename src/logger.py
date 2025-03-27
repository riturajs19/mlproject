import logging  # Enables logging of program execution. Used to record events (INFO, WARNING, ERROR,DEBUG)
import os  # Provides functionalities to interact with the operating system
from datetime import datetime  # Used to generate timestamps for log files

# Step 1: Create a unique log filename based on the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
#.strftime('%m_%d_%Y_%H_%M_%S'): Formats the date/time as MM_DD_YYYY_HH_MM_SS.
#Why? This ensures each log file has a unique name, preventing overwrites.
#Example - 03_27_2025_15_30_45.log


# Step 2: Define the path where log files will be stored
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
#os.getcwd(): Gets the current working directory.
#"logs": Specifies that logs should be stored inside a logs folder.
#LOG_FILE: Adds the unique log filename.
#Why? This ensures that logs are organized and stored properly.
#Example - C:\Users\YourName\YourProject\logs\03_27_2025_15_30_45.log


# Step 3: Ensure the "logs" directory exists; if not, create it
os.makedirs(logs_path, exist_ok=True)

# Step 4: Define the full path of the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Step 5: Configure logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Save logs to this file
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Format of logs
    level=logging.INFO  # Set logging level to INFO (captures info, warnings, errors, etc.)
)
#filename=LOG_FILE_PATH → Saves logs in the generated log file.
#format="..." → Defines how each log entry looks.
#level=logging.INFO → Captures INFO, WARNING, ERROR, and CRITICAL logs.

#%(asctime)s → Timestamp of log event (e.g., [2025-03-27 15:30:45]).
#%(lineno)d → Line number where the log was generated.
#%(name)s → Name of the logger (by default, the root logger).
#%(levelname)s → Log severity (INFO, WARNING, ERROR, etc.).
#%(message)s → The actual log message.

# Step 6: Create a log entry when the script runs
if __name__ == "__main__":
    logging.info("Logging has started")
