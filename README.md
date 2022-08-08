# The end of a journey.
It's been fun developing this bot along with the others.

Many things are still unfinished, so if you're gonna pick this project back up, keep that in mind.

Also note: both the code and the commit naming are shitshows.



## Old readme

<details>
<summary>
Old README.md
</summary>

# AOUutils.py
## Setup

- get python 3.9.5
- Make a venv (use pycharm)
- run `pip install -U git+https://github.com/Rapptz/discord.py` inside the venv terminal.
- install all needed libraries
- run the bot

## Running
- Run the file called `setup.bat` for first time launches.

- now run the bot, you may use the run button
  
![the run button](https://cdn.discordapp.com/attachments/867110109733847120/867757152546062356/54ZcU6Z3y.png)

## Features
* items with a `*` next to them is optional
* items with a `**` next to them is experimental
* items with a <i style="font-size: 75%;">TBD</i> next to them is to be determined, may or may not happen.

| Feature           | Usage                                                                                                                | Permissions*                                                                         |
|-------------------|----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Coloured Console  | Items printed to console <br>can be coloured using the <br>crayons module                                            |                                                                                      |
| Info logs         | Loggers for info, ready up, <br> etc make debugging a lot <br>easier                                                 |                                                                                      |
| jishaku           | Jishaku is a debugging <br>cog made for discord bots<br> running `aou jsk py code` <br> will evaluate the given code | owner of bot                                                                         |
| moderation        | other moderation bots no <br>longer needed! with AOUutils<br>every other bot becomes <br>useless!                    | depends on<br>command                                                                |
| API               | a full API for interacting with <br>AOU and AOUutils**                                                               | API Key <i style="font-size: 75%; position:relative; top: -5px; left: -4px;">TBD</i> |
| Currency System** | Full on dank-memer like currency<br>system!                                                                          | existance                                                                            |

## Known errors when running:
### `NoneType` Has no attribute `member_count`
- you can safely ignore this one, its due to the bot you are running not being in AOU, as a result, being unable to fetch its member count.


</details>
