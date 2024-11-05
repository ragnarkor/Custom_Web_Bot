# Auto Booking Web Bot for SmartPlay

## Table of Contents
- [Overview](#Overview)
- [Installation](#installation)
- [Usage](#usage)


## Overview

**Auto Booking Web Bot for SmartPlay** is an automation tool leverages Selenium to streamline the booking process on the SmartPlay platform, allowing users to secure their desired slots effortlessly and efficiently.


## Installation

To get started with the Auto Booking Web Bot, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/TimLL123456/Web_Bot.git
    cd Web_Bot/Smart_Play_Bot
    ```

2. **Install Dependencies**:

    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Configuration**:

    The bot can be configured through a config.yaml file. Here’s an example configuration:
    ```yaml
    username: "12312312"
    password: "12312312312"
    booking_month: 11
    booking_day: 10
    timeslot: "上午7時"
    venue: "竹園體育館"
    cardholder: "Chan Tai Man"
    card_num: "5419281455243022"
    expiry_month: "07"
    expiry_year: "23"
    security_code: "000"
    ```
    Make sure to update the configuration file with your details before running the bot.

## Usage
To run the bot, execute the following command in your terminal:
```bash
python smart_play_bot.py
```