<img width="150" height="150" align="left" style="float: left; margin: 0 10px 0 0;" alt="Auxilium" src="https://cdn.discordapp.com/app-icons/619670204506701829/e0ca67b591d30e8b54c8044f0e702e4c.png">  

# Auxilium

(https://img.shields.io/discord/85398421053116416.svg?logo=discord&colorB=7289DA&logoColor=white)
[![GitHub last commit](https://img.shields.io/github/last-commit/richardyang/AuxiliumBot.svg?style=flat)](https://github.com/richardyang/AuxiliumBot)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/richardyang/AuxiliumBot/blob/master/LICENSE)
<!-- [![](https://img.shields.io/badge/discord.js-v12.0.0--dev-blue.svg?logo=npm)](https://github.com/discordjs) -->
> Auxilium is the first-ever open source Discord bot with features powered by machine learning. 
------

This repository is the public release version of Auxilium, written in Python using the [Discord.py](https://discordpy.readthedocs.io/en/latest/) API. 

[Features](#features) · [Installation](#installation) · [Support](#support) · [License](#license)

## Features
Auxilium (AUX) is modular, so you can only enable the features you need. Currently there are 3 components, but we love collaborators to help extend our bot even further!
1. [AUX Core](#aux-core): The core features of AUX, including an leveling system, economy, utilities, and other fun commands.
2. [AUX Theta](#aux-theta): The machine learning powered features of AUX. You can talk to a conversational AI powered by the OpenAI GPT-2 language model.
3. [AUX FFXIV](#aux-ffxiv): Helpful features specifically for Final Fantasy XIV. Link your Discord profile to your FFXIV character, search the market board, and more!

Some highlights of the bot are shown below. For the full list of functionality, type `-help` for more information once it is in your server.

### AUX Core
___
Core includes a lot of utilities to supercharge your chat and make it fun. Core also serves as a bridge between the Discord API and your choice of a SQLite or remote MySQL database to store data about your server. You can turn your Discord chat into a game by enabling leveling and economy. Each message a user posts will earn them some experience points and coins.

![](https://cdn.discordapp.com/attachments/691876919095853069/694040149855567892/unknown.png)

Every user on your server will also get an integrated profile:

![](https://cdn.discordapp.com/attachments/691876919095853069/694035683492364308/unknown.png)

Core also comes with an gametime tracker, inspired by Xfire/Steam. You can see what your personal and the guild's top games are.

![](https://cdn.discordapp.com/attachments/691876919095853069/694039893512290374/unknown.png)

Another fun feature is the battle system that allows users to virtually battle each other using random skills from your favorite games. All skills and damage are completely random, so it's just for fun! This is an expanded version of Yggdrasil bot's [death-battle feature](https://ygg.fun/). You can specify custom classes and skills, and users can choose their own class before battling.

![](https://cdn.discordapp.com/attachments/394019091024707584/694047495705198682/battle.gif)

Other features include an 8-ball, upvotes/downvotes, awards, and random utilities for your chat! Check out the help document for a list of all the features.

### AUX Theta
___
Theta is the module for all services powered by machine learning. Currently, we've implemented a conversational AI using a transfer learning technique by [HuggingFace](https://medium.com/huggingface/how-to-build-a-state-of-the-art-conversational-ai-with-transfer-learning-2d818ac26313) using a pre-trained GPT-2 language model from OpenAI.

![](https://i.imgur.com/Yjbw8sk.gif)

A work-in-progress feature is a language translation tool using deep learning models. Stay tuned for more info!

### AUX FFXIV
___
FFXIV contains helpful utilities specifically for Final Fantasy XIV. It pulls information from the Lodestone and the XIV API.

![](https://i.imgur.com/h8nPhSU.png)

Users can link their character to the bot, and all information displayed will be geared toward their character and server. For example, when a user searches for an item, the market prices will be shown for their server.

![](https://cdn.discordapp.com/attachments/694045222916587541/694093536538263552/unknown.png)

Other features include character level tracking, achievements, and crafting recipes. Check out the help document for a list of all the features.

## Installation
This bot is currently self-hosted only, with a public beta planned in 2020. These instructions are for you to host your own bot.
1. Create an application in the Discord developer portal and obtain the token. You can follow this handy instruction guide: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
2. Install Python 3.6+, we suggest using Anaconda: https://www.anaconda.com/distribution/#download-section
3. Clone this repository on the machine you are hosting the bot
4. Install dependencies by running `pip install -r ext/requirements.txt`. This will install the dependencies for ALL components. If you don't want to use all of the components, you can install the partial dependencies by running `pip install -r ext/req_COMPONENT.txt` and replace COMPONENT in the filename with the one you want (e.g. Core, Theta, FFXIV).
5. Edit the `CONFIG` file with your favorite text editor, and follow the instructions outlined in the file to properly configure your bot.
6. Start the bot using `python run.py` in the root directory.
7. [ADVANCED/OPTIONAL] By default, AUX stores data in a SQLite database. If you have a large server, you may want to set up a dedicated MySQL database. Once done, you can fill out the connection information in the `CONFIG` file. 

## Support
If you need any assitance with the bot, find any bugs, or would to request a new feature, please join our Discord server: https://discord.gg/YSntuFn


## License
Auxilium is licensed under the MIT License. See the LICENSE file for more information.
