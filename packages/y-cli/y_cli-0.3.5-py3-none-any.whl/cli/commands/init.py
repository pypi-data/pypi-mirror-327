import os
import click
from config import config, CONFIG_FILE
from bot import BotConfig
from config import bot_service

def print_config_info():
    """Print configuration information and available settings."""
    click.echo(f"\n{click.style('Configuration saved to:', fg='green')}\n{click.style(CONFIG_FILE, fg='cyan')}")
    click.echo(f"{click.style('Chat data will be stored in:', fg='green')}\n{click.style(config['chat_file'], fg='cyan')}")
    click.echo(f"{click.style('Bot config data will be stored in:', fg='green')}\n{click.style(config['bot_config_file'], fg='cyan')}")
    click.echo(f"{click.style('MCP server config data will be stored in:', fg='green')}\n{click.style(config['mcp_config_file'], fg='cyan')}")
    
    click.echo(f"\n{click.style('Optional settings that can be configured using `y-cli bot add`:', fg='green')}")
    click.echo(f"- {click.style('model:', fg='yellow')} The model to use for chat")
    click.echo(f"- {click.style('base_url:', fg='yellow')} OpenRouter API base URL")
    click.echo(f"- {click.style('print_speed:', fg='yellow')} Speed of text printing")
    click.echo(f"- {click.style('description:', fg='yellow')} Bot configuration description")
    click.echo(f"- {click.style('openrouter_config:', fg='yellow')} OpenRouter configuration settings")
    click.echo(f"- {click.style('mcp_servers:', fg='yellow')} Model Context Protocol settings")
    click.echo(f"- {click.style('max_tokens:', fg='yellow')} Maximum number of tokens in response")
    click.echo(f"- {click.style('custom_api_path:', fg='yellow')} Custom path for chat completion API request")
    
    click.echo(f"\n{click.style('MCP servers can be configured using `y-cli mcp add` with these settings:', fg='green')}")
    click.echo(f"- {click.style('name:', fg='yellow')} Name of the MCP server")
    click.echo(f"- {click.style('command:', fg='yellow')} Command to execute the server (e.g., 'node', 'python')")
    click.echo(f"- {click.style('args:', fg='yellow')} Command line arguments for the server")
    click.echo(f"- {click.style('env:', fg='yellow')} Environment variables for the server process")

    click.echo(f"\n{click.style(f'Proxy settings can be configured in {CONFIG_FILE}:', fg='magenta')}")
    click.echo(f"- {click.style('proxy_host/proxy_port:', fg='yellow')} Network proxy settings")

@click.command()
def init():
    """Initialize y-cli configuration with required settings.

    Creates a config file then prompts for required settings.
    """
    # Get existing default config or create new one
    default_config = bot_service.get_config()
    
    # If already initialized with API key, skip to echo
    if default_config and default_config.api_key:
        print_config_info()
        return

    # Prompt for OpenRouter API key if not initialized
    api_key = click.prompt(
        "Please enter your OpenRouter API key",
        type=str,
        default=default_config.api_key,
        show_default=False
    )

    # Create new config with updated API key
    new_config = BotConfig(
        name="default",
        api_key=api_key,
        base_url=default_config.base_url,
        model=default_config.model,
        print_speed=default_config.print_speed,
        description=default_config.description,
        mcp_servers=default_config.mcp_servers
    )

    # Update the default config
    bot_service.add_config(new_config)

    print_config_info()
