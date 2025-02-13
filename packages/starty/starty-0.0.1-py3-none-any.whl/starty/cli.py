import os
import click
import shutil
import functools
from colorama import Fore, Style
from .utils import success, warning, error

@click.group()
def cli():
    """Starty - Python web management."""
    pass

@cli.command()
def createapp():
    """Create a new application."""
    app_name = input(f"{Fore.YELLOW}[ ! ] Insert the name of the app: {Style.RESET_ALL}")
    
    if not app_name.strip():
        error("Invalid app name!")
        return
    
    if os.path.exists(app_name):
        error(f"The folder '{app_name}' already exists!")
        return
    
    try:
        # Create the app folder
        os.makedirs(app_name)
        
        # Create the templates subfolder
        templates_folder = os.path.join(app_name, "templates")
        os.makedirs(templates_folder)
        
        # Create a default index.html
        index_html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My App</title>
</head>
<body>
    <h1>Welcome to My App!</h1>
    <p>This is the default index.html served directly on localhost.</p>
</body>
</html>
'''
        index_html_path = os.path.join(templates_folder, "index.html")
        with open(index_html_path, "w") as f:
            f.write(index_html_content)
        
        # Create manager.py with a CustomHandler
        manager_content = '''#!/usr/bin/env python3
"""
Manager script to run a simple local server that serves the templates directory,
automatically displaying index.html when the root is requested.
"""

if __name__ == '__main__':
    import http.server
    import socketserver
    import functools

    PORT = 8000

    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/index.html'
            return super().do_GET()

    # Serve the 'templates' folder as the root directory
    Handler = functools.partial(CustomHandler, directory="templates")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at http://localhost:8000")
        httpd.serve_forever()
'''
        manager_path = os.path.join(app_name, 'manager.py')
        with open(manager_path, 'w') as f:
            f.write(manager_content)
        
        success(f"Folder '{app_name}' created successfully with manager.py and templates/index.html!")
    except Exception as e:
        error(f"Error creating folder, templates, or manager.py: {e}")

@cli.command()
def deleteapp():
    """Delete an existing application."""
    app_name = input(f"{Fore.YELLOW}[ ! ] Insert the name of the app to delete: {Style.RESET_ALL}")
    
    if not app_name.strip():
        error("Invalid app name!")
        return

    if not os.path.exists(app_name):
        error(f"The folder '{app_name}' does not exist!")
        return

    try:
        shutil.rmtree(app_name)
        success(f"Folder '{app_name}' deleted successfully!")
    except Exception as e:
        error(f"Error deleting folder: {e}")

@cli.command()
def startapp():
    """Start the local server for an existing application."""
    app_name = input(f"{Fore.YELLOW}[ ! ] Insert the name of the app to start: {Style.RESET_ALL}")
    
    if not app_name.strip():
        error("Invalid app name!")
        return
    
    if not os.path.exists(app_name):
        error(f"The folder '{app_name}' does not exist!")
        return

    try:
        # Move into the app folder
        os.chdir(app_name)

        # -- USIAMO LO STESSO CUSTOM HANDLER DI manager.py --
        import http.server
        import socketserver
        import functools

        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.path = '/index.html'
                return super().do_GET()

        Handler = functools.partial(CustomHandler, directory="templates")

        PORT = 8000
        print(f"{Fore.GREEN}[✅] Serving at http://localhost:{PORT} (Press Ctrl+C to stop)")
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        warning("Server stopped by user.")
    except Exception as e:
        error(f"Error starting the server: {e}")
