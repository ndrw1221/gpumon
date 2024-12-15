# gpumon

## Overview
**gpumon** is a Python-based GPU monitoring tool that tracks the available memory on GPUs and sends email notifications when the free memory exceeds a specified threshold. This tool is particularly useful for machine learning and deep learning practitioners who need to optimize GPU usage in shared environments.

## Features
- Monitors GPU memory usage using `nvidia-smi`
- Sends email notifications when free memory exceeds a customizable threshold
- Configurable check intervals
- Logs GPU memory statistics to a log file

## Requirements
- Python 3.8 or higher
- NVIDIA GPUs with `nvidia-smi` installed
- SMTP server credentials for email notifications

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/gpumon.git
   cd gpumon
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set up the environment variables for email notifications:
   ```bash
   export SENDER_EMAIL=your_email@gmail.com
   export RECEIVER_EMAIL=receiver_email@gmail.com
   export EMAIL_PASSWORD=your_password
   ```

2. Run the script:
   ```bash
   python gpumon.py
   ```

3. Adjust the configuration as needed:
   - `MEMORY_THRESHOLD`: The free memory threshold for notifications (in MiB). Default is 20480 (20GB).
   - `CHECK_INTERVAL`: The interval between checks (in seconds). Default is 60 seconds.


## Logging
Logs are stored in `gpu_monitor.log` and include:
- Timestamp (Asia/Taipei timezone)
- GPU memory statistics
- Notification events

## Troubleshooting
- **Error: `nvidia-smi` command not found**: Ensure that NVIDIA drivers and CUDA Toolkit are installed, and `nvidia-smi` is in your system's PATH.
- **Email notification not working**: Verify that the sender's email has SMTP access enabled. For Gmail, you may need to use an App Password.
- **Environment variables not set**: Make sure `SENDER_EMAIL`, `RECEIVER_EMAIL`, and `EMAIL_PASSWORD` are correctly configured in your environment.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request to improve this project.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
