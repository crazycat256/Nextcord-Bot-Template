# Nextcord-Bot-Template

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Built-in Functionalities](#built-in-functionalities)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This is a template for a Discord bot written in Python using the [Nextcord](https://nextcord.dev/) library. It provides a basic structure for your bot project, as well as examples of commands/events/tasks, utilities and more.

## Prerequisites

- [Python](https://www.python.org/downloads/) 3.8 or higher
- A [bot account](https://docs.nextcord.dev/en/stable/discord.html) and token
- Basic knowledge of Python and Discord

## Getting Started

1. Click on the "Use this template" button at the top of the GitHub page to create a new repository based on this template.
2. Clone your new repository locally: `git clone https://github.com/yourusername/your-bot-repo.git`
3. Navigate to the cloned repository: `cd your-bot-repo`
4. Create a virtual environment (recommended):
    - On Windows: `python -m venv venv`
    - On Linux/macOS: `python3 -m venv venv`
5. Activate the virtual environment:
    - On Windows: `venv\Scripts\activate`
    - On Linux/macOS: `source venv/bin/activate`
6. Install dependencies: `pip install -r requirements.txt`
7. Rename `.env.example` to `.env` and add your bot's token.
8. Add your test server's ID to the config.py file.
9. Run the bot using `python3 main.py`.

## Built-in Functionalities

### Cogs Handler

The bot handles commands, events, and tasks using cogs. This allows you to easily organize your code into separate files and folders. The cogs directory can be defined by setting the `COGS_DIR` variable in the `config.py` file.

### Auto Reload

The bot can automatically reload commands, events, and tasks when they are modified. This is useful for testing changes without having to restart the bot.
This feature can be enabled/disabled by setting the `AUTO_RELOAD` variable in the `config.py` file.

### Views

- `ConfirmButtons`: A view that displays a confirmation message with two buttons.
- `PageButtons`: A view that displays a paginated message with buttons to navigate between pages.

### Logging

The bot has a built-in `Logger` class that can be used to log messages to the console and a log file.

## Creating Cogs

To create a new cog, create a new file in the cogs directory, create a class that inherits from `nextcord.ext.commands.Cog` and a `setup` function that adds the cog to the bot. Then, add your commands, events, and tasks to the cog. Read the [Nextcord cogs documentation](https://docs.nextcord.dev/en/latest/ext/commands/api.html#nextcord.ext.commands.Cog) for more information. Here are some examples:

### Command

```py
from config import *
from bot import Bot
from nextcord import Interaction, slash_command
from nextcord.ext.commands import Cog

class ExampleCommand(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(description="Example command", guild_ids=GUILD_IDS)
    async def example_command(self, interaction: Interaction, ...): # Replace ... with your command parameters
        pass # Your code here

def setup(bot: Bot):
    bot.add_cog(ExampleCommand(bot))
```

### Event

```py
from config import *
from bot import Bot
from nextcord.ext.commands import Cog
from nextcord.ext import commands

class ExampleEvent(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener("event_name") # Replace event_name with the event name
    async def example_event(self, ...): # Replace ... with the event parameters
        pass # Your code here

def setup(bot: Bot):
    bot.add_cog(ExampleEvent(bot))
```

Note: You can find a list of events [here](https://nextcord.readthedocs.io/en/latest/api.html#event-reference).

### Task

```py
from config import *
from bot import Bot
from nextcord.ext.commands import Cog
from nextcord.ext import tasks

class ExampleTask(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @tasks.loop(seconds=30) # Put the interval here using seconds, minutes or hours
    async def example_task(self):
        await self.bot.wait_until_ready() # This prevents the task from running before the bot is ready
        # Your code here
                
    @example_task.error
    async def on_error(self, exception: Exception):
        await self.bot.handle_task_error(exception, "example_task") # This will log the error and print it to the console

def setup(bot: Bot):
    bot.add_cog(ExampleTask(bot))
```

## Contributing

Contributions are welcome! If you have any suggestions or find any bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this code as long as you give credit to the original author and include the license.
See the [LICENSE](LICENSE) file for details.
