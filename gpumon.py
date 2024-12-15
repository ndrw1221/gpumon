import subprocess
import logging
import time
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
from pytz import timezone

# Define memory threshold (in MiB)
MEMORY_THRESHOLD = 20480  # 20GB in MiB
CHECK_INTERVAL = 60  # Check every 60 seconds
TIMEZONE = "Asia/Taipei"


# Set timezone to Asia/Taipei
def timetz(*args):
    return datetime.now(tz).timetuple()


tz = timezone(TIMEZONE)
logging.Formatter.converter = timetz

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("gpu_monitor.log"),
    ],
)


# Function to fetch GPU usage
def get_gpu_memory():
    try:
        # Run nvidia-smi command
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        # Parse the output and convert to integers
        free_memory = list(map(int, result.stdout.strip().split("\n")))
        return free_memory
    except Exception as e:
        logging.error(f"Error fetching GPU memory: {e}")
        return []


# Function to send email notification
def send_notification(gpu_id, free_memory):
    try:
        sender_email = os.environ.get("SENDER_EMAIL")
        receiver_email = os.environ.get("RECEIVER_EMAIL")
        password = os.environ.get("EMAIL_PASSWORD")

        if not sender_email or not receiver_email or not password:
            logging.error("Email credentials are not set in environment variables.")
            return

        subject = f"GPU {gpu_id} Available"
        body = f"GPU {gpu_id} has {free_memory} MiB of free memory available."

        # Explicitly use UTF-8 encoding for the email
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        logging.info(f"Notification sent for GPU {gpu_id}")
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"SMTP Authentication Error: {e}")
        logging.error(
            "Ensure that 'Allow less secure apps' is enabled in your Google account or use an App Password."
        )
    except Exception as e:
        logging.error(f"Failed to send notification: {e}")


def monitor_gpus():
    notified_gpus = set()

    while True:
        free_memory = get_gpu_memory()
        available_gpus = []

        if free_memory:
            for gpu_id, mem in enumerate(free_memory):
                logging.info(f"GPU {gpu_id}: {mem} MiB free memory.")

                if mem >= MEMORY_THRESHOLD and gpu_id not in notified_gpus:
                    available_gpus.append(gpu_id)

            if available_gpus:
                gpu_list = ", ".join(map(str, available_gpus))
                logging.info(
                    f"GPUs {gpu_list} meet the threshold. Sending notification..."
                )
                send_notification(
                    gpu_list,
                    ", ".join([f"{free_memory[gpu]} MiB" for gpu in available_gpus]),
                )
                notified_gpus.update(available_gpus)

            for gpu_id in list(notified_gpus):
                if free_memory[gpu_id] < MEMORY_THRESHOLD:
                    logging.info(
                        f"GPU {gpu_id} no longer meets the threshold. Resetting notification status."
                    )
                    notified_gpus.remove(gpu_id)
        else:
            logging.error("Failed to fetch GPU data.")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_gpus()
