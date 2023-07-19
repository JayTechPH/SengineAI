# SengineAI

![Project Logo](bot.png)

This is a Python script that automates sending greetings on Facebook Messenger.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Educational Purpose](#educational-purpose)

## Requirements

- Python 3.x
- undetected_chromedriver
- selenium

## Installation

1. Clone the repository:

```shell
git clone https://github.com/JayTechPH/SengineAI.git

2. Install the dependencies:

```shell
pip install undetected_chromedriver selenium
```

## Usage

1. Initialize the `facebook_bot` class with your configuration:

```python
bot = facebook_bot(gcid, username, password, morning, evening, afternoon, night)
```

2. Run the script:

```shell
python main.py
```

The script will log in to Facebook Messenger and send greetings based on the specified times.

## Configuration

You need to provide the following configuration parameters when initializing the `facebook_bot` class:

- `gcid`: The ID of the group chat on Facebook Messenger.
- `username`: Your Facebook username or email.
- `password`: Your Facebook password.
- `morning`: The time in 24-hour format when the "Good Morning" greeting should be sent (e.g., "08:00:00").
- `evening`: The time in 24-hour format when the "Good Evening" greeting should be sent (e.g., "18:00:00").
- `afternoon`: The time in 24-hour format when the "Good Afternoon" greeting should be sent (e.g., "13:00:00").
- `night`: The time in 24-hour format when the "Good Night" greeting should be sent (e.g., "22:00:00").

Feel free to customize the greetings and add more functionality to the script as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
We welcome contributions from the community. To contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

## Educational Purpose

This project is intended for educational purposes only. It serves as a demonstration of how to automate certain tasks using Python and the [selenium](https://pypi.org/project/selenium/) library. The 
code provided here should be used responsibly and in accordance with the terms and conditions of the platforms or applications it interacts with. The project 
authors and contributors are not responsible for any misuse or illegal activities performed using this project.
