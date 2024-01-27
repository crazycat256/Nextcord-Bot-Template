import config as _config
import nextcord as _nextcord
import traceback as _traceback
import os as _os




async def success(interaction: _nextcord.Interaction, message: str, ephemeral: bool = True):
    """|coro|
    
    Send a success message to an interaction

    Parameters
    ----------
    interaction: :class:Interaction
        The interaction to respond to
    message: :class:`str`
        The message to send
    ephemeral: :class:`bool`
        If the response is only visible to the user, by default True
    """
    embed = _nextcord.Embed(description=f"**Success**: {message}", color=_nextcord.Color.green())
    await interaction.send(embed=embed, ephemeral=ephemeral)

    
async def warn(interaction: _nextcord.Interaction, message: str, ephemeral: bool = True):
    """|coro|
    
    Send a warning message to an interaction

    Parameters
    ----------
    interaction: :class:Interaction
        The interaction to respond to
    message: :class:`str`
        The message to send
    ephemeral: :class:`bool`
        If the response is only visible to the user, by default True
    """
    embed = _nextcord.Embed(description=f"**Warning**: {message}", color=_nextcord.Color.gold())
    await interaction.send(embed=embed, ephemeral=ephemeral)


async def error(interaction: _nextcord.Interaction, message: str, ephemeral: bool = True):
    """|coro|
    
    Send an error message to an interaction
    
    Parameters
    ----------
    interaction: :class:Interaction
        The interaction to respond to
    message: :class:`str`
        The message to send
    ephemeral: :class:`bool`
        If the response is only visible to the user, by default True
    """
    embed = _nextcord.Embed(description=f"**Error**: {message}", color=_nextcord.Color.red())
    await interaction.send(embed=embed, ephemeral=ephemeral)


def get_traceback(exception: Exception) -> str:
    """Returns the traceback string from an exception
    
    Parameters
    ----------
    exception: :class:`Exception`
        The exception to get the traceback from
        
    Returns
    -------
    :class:`str`
        The traceback of the exception
    """
    return "".join(_traceback.format_exception(exception.__class__, exception, exception.__traceback__))


def get_command(data: dict) -> str:
    """Returns the command string from a slash command data
    
    Parameters
    ----------
    data: :class:`dict`
        The data of the slash command, from :attr:`Interaction.data`
    
    Returns
    -------
    :class:`str`
        The command string
    """
    res = data.get("name", "")
    if "options" in data:
        for option in data["options"]:
            res += " " + get_command(option)
    if "value" in data:
        res += ":" + str(data["value"])
    return res


def file_to_module(root: str, filepath: str) -> str:
    """Converts a filepath to a module path
    
    Parameters
    ----------
    root: :class:`str`
        The root directory
    filepath: :class:`str`
        The filepath to convert
        
    Returns
    -------
    :class:`str`
        The module path
    """
    return _os.path.join(root, filepath).removesuffix(".py").replace("\\", ".").replace("/", ".")


def module_to_file(filepath: str) -> str:
    """Converts a module path to a filepath
    
    Parameters
    ----------
    filepath: :class:`str`
        The module path to convert
        
    Returns
    -------
    :class:`str`
        The filepath
    """
    return filepath.replace(".", _os.sep) + ".py"


def get_cogs():
    """Returns a set of all the cogs
    
    Returns
    -------
    :class:`set`
        The set of all the cogs
    """
    cogs = set()
    for root, dirs, files in _os.walk(_config.COGS_DIR):
        if not root.startswith("__"):
            for file in files:
                if file.endswith(".py") and file not in _config.LOAD_EXCEPTIONS:
                    cogs.add(file_to_module(root, file))
    return cogs



