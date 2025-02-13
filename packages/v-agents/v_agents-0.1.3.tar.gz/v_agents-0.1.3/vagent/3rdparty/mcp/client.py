import asyncio
from typing import Optional, Any, Dict, List
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import mcp.types as types

class MCPClient:
    """A client class for interacting with MCP servers."""
    
    def __init__(self):
        """Initialize the MCP client."""
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tools_cache: Dict[str, types.Tool] = {}
        
    async def connect_to_server(self, server_command: str, args: List[str] = None, env: Dict[str, str] = None) -> None:
        """Connect to an MCP server.
        
        Args:
            server_command: The command to start the server (e.g., "python", "node")
            args: Optional list of arguments for the server
            env: Optional environment variables for the server
        """
        server_params = StdioServerParameters(
            command=server_command,
            args=args or [],
            env=env
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        # Initialize the connection
        await self.session.initialize()
        
        # Cache available tools
        tools_response = await self.session.list_tools()
        self.tools_cache = {tool.name: tool for tool in tools_response.tools}
        
        print(f"Connected to server with tools: {list(self.tools_cache.keys())}")
    
    async def list_tools(self) -> List[types.Tool]:
        """List all available tools from the server."""
        if not self.session:
            raise RuntimeError("Not connected to a server")
        
        response = await self.session.list_tools()
        return response.tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> types.CallToolResult:
        """Call a specific tool with given arguments.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Dictionary of arguments to pass to the tool
            
        Returns:
            The result from the tool execution
        """
        if not self.session:
            raise RuntimeError("Not connected to a server")
            
        if tool_name not in self.tools_cache:
            raise ValueError(f"Tool '{tool_name}' not found. Available tools: {list(self.tools_cache.keys())}")
            
        return await self.session.call_tool(tool_name, arguments)
    
    async def list_resources(self) -> List[types.Resource]:
        """List all available resources from the server."""
        if not self.session:
            raise RuntimeError("Not connected to a server")
            
        response = await self.session.list_resources()
        return response.resources
    
    async def read_resource(self, uri: str) -> types.ReadResourceResult:
        """Read a specific resource by URI.
        
        Args:
            uri: URI of the resource to read
            
        Returns:
            The content of the resource
        """
        if not self.session:
            raise RuntimeError("Not connected to a server")
            
        return await self.session.read_resource(uri)
    
    async def list_prompts(self) -> List[types.Prompt]:
        """List all available prompts from the server."""
        if not self.session:
            raise RuntimeError("Not connected to a server")
            
        response = await self.session.list_prompts()
        return response.prompts
    
    async def get_prompt(self, name: str, arguments: Dict[str, Any] = None) -> types.GetPromptResult:
        """Get a specific prompt with optional arguments.
        
        Args:
            name: Name of the prompt to get
            arguments: Optional dictionary of arguments for the prompt
            
        Returns:
            The prompt result
        """
        if not self.session:
            raise RuntimeError("Not connected to a server")
            
        return await self.session.get_prompt(name, arguments)
    
    async def cleanup(self):
        """Clean up resources and close the connection."""
        await self.exit_stack.aclose()