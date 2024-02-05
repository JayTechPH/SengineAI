<p align="center">
  <img width="250" height="250" src="https://media.tenor.com/nJCX4ZuO4OkAAAAi/dancing-dance-moves.gif">
</p>
<h1 align="center">SengineAI</h1><p align="center">
<b>SengineAI</b> is <b>Facebook Messenger Bot</b> Like Discord Bot.
</p>   

<p align=center>  
<a href="https://github.com/JayTechPH"><img src="https://img.shields.io/badge/Author-JayTechPH-red.svg?style=for-the-badge&label=Author" /></a>

<img src="https://img.shields.io/badge/Version-2.0-brightgreen?style=for-the-badge" >
<img src="https://img.shields.io/github/stars/JayTechPH/SengineAI?style=for-the-badge">  
<img src="https://img.shields.io/github/followers/JayTechPH?label=Followers&style=for-the-badge">
</p>   

* **If you like the tool and for my personal motivation so as to develop other tools please leave a +1 star** 

This Python script is developed as an unofficial Facebook Messenger bot, similar to a Discord bot in functionality and versatility. It enables automated interactions within Facebook Messenger chats, offering features such as responding to specific user commands and sending automated messages. The bot can be customized to suit the specific needs of its users or groups through programming in Python and adding functions, making it a powerful tool for enhancing communication and engagement on the Facebook Messenger platform.

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
```

2. Install the dependencies:

```shell
pip install beautifulsoup4
pip install selenium
pip install undetected-chromedriver
```

## Usage

1. Set the `username` and `password` in main.py:

```python
import Sengine.SengineAI as sg

fb = sg.SengineAI()

username = "set_username_here"
password = "set_password_here"

fb.login(username, password)
```

2. Run the script:

```shell
python main.py
```

The script will log in to Facebook Messenger and send greetings based on the specified times.

## Configuration
You need to provide the `username` and `password` in main.py, and you can add a custom command to config.json.

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
