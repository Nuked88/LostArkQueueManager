<p align="center"><img alt="Logo" src="https://raw.githubusercontent.com/Nuked88/LostArkQueueManager/main/doc/Logo.jpg"></p>

<h1 align="center">Welcome to Lost Ark Queue Manager 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.8-blue.svg?cacheSeconds=2592000" />
  <a href="http://www.apache.org/licenses/LICENSE-2." target="_blank">
    <img alt="License: Apache 2.0" src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" />
  </a>
  <a href="https://twitter.com/Nuked" target="_blank">
    <img alt="Twitter: Nuked" src="https://img.shields.io/twitter/follow/Nuked.svg?style=social" />
  </a>
</p>

Manage Queue in **Lost Ark** and join automatically in your default server
The Queue manager will send you info about the status of the queue via telegram bot.
The check of the queue **will work** even if **Lost Ark** is minimized!
## :ghost: Limitation

* The **Auto-Join-to-server*** feature will **ONLY** work if the name of your server is visible on the main page of the screen list and will **NOT** work, for example, if you need to scroll the list for see and join to it
* I've tried to generate an executable from this projext but was **INSANELY BIG** (like 2.5 GB) so for now we will continue to use the python script

## :rocket: Install
* Install python 3.8 or better if you doesn't already have it on your pc ( Download it <a href="https://www.python.org/ftp/python/3.9.10/python-3.9.10-amd64.exe">HERE</a> and make sure to check **Add Python 3.x to PATH** - <a href="https://raw.githubusercontent.com/Nuked88/LostArkQueueManager/main/doc/Install-Python-Windows-Step-1.png">example here</a> )
* Clone this repository (or download it from <a href="https://github.com/Nuked88/LostArkQueueManager/archive/refs/heads/main.zip">here</a> and extract everything in a folder you like)
* Run the following command at the root of your project
  ```sh
  pip -r requirements.txt
  ```
  or click on **install.bat**

## :wrench: First Configuration
* Go in the **targets** folder, you will see three images, these are screen that i have taken from my game (witch is runnning in 2k), for make this program been able to work propriety you will need to replace it with your images if you see that is not working well:

  * `button.png` (**mandatory**) is the button that appear on the popup when you are in queue 
  * `launch.png` is the button that appear when the queue is over and you can enter in your server (**mandatory** if you want to use the **Auto-Join-to-server**  feature)
  * `exit_eac.png` (mine is in italian) is the button that appean when the game fail to start (it's happen to me **EVERYTIME** i launch the game the first time after a  reboot of my pc, if you doesn't have this issue you can ignore that...)

**TIPS: To take a screenshot on a specific part of the screen on Windows 10 or 11 press the <kbd> Shift </kbd> + <kbd> Win </kbd> + <kbd> S</kbd>   buttons and then save the image**
  <br>
* Rename `config.example.yaml` in `config.yaml`, open it and configure it as follow:
  * **[Telegram notification]** Retrive your chat id following <a href="https://www.alphr.com/find-chat-id-telegram/">this instruction</a>  and put it in the   `bot_chatID` field (replace **00000000** maintaining the **"**  **"**), otherwise leave it like so or set it to **None**
  * **[Telegram notification]** Put in `send_message_under` field when the bot should start to send you notification on telegram `Default: 400`
  * **[Telegram notification]** Put in `check_queue_time` field how often (seconds) the bot will notify you (and the program will check the Lost Ark queue) `Default:   30`
  * Put in `server_name` field the name of your server or leave it empty if you just doesn't want the **Auto-Join-to-server** feature
* Enjoy!
## :clipboard: Usage

If you want to just launch this program double click on
```sh
main.pyw
```

If you just want to run the Queue Manager because the game is already running run: 
```sh
main.pyw c
```
or double-click on **RunQueueManager.bat**

If you want automatically run LostarK an then the the Queue Manager run: 

```sh
main.pyw gc
```
or double-click on **RunGameAndQueueManager.bat**



## Author

👤 **Nuked**

* Twitter: [@Nuked](https://twitter.com/Nuked)
* Github: [@Nnuked88](https://github.com/Nuked88)

## 🤝 Contributing
Contributions, issues and feature requests are welcome!
Feel free to check [issues page](https://github.com/Nuked88/LostArkQueueManager/issues). 


## Show your support
:heart: Give a ⭐️ if this project helped you! :heart:

:heart:  [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C0AJECJ)  :heart:

## 📝 License

Copyright © 2022 [Nuked](https://github.com/Nuked88).
This project is [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0) licensed.
