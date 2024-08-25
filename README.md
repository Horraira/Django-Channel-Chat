Chat Website with Django and Django Channels
============================================

This tutorial will guide you through creating a chat website using Django and Django Channels.

Getting Started
---------------

### 1\. Setting up a Django Project

1.  Create and enter the desired directory for project setup.
    
2.  pipenv shell
    
3.  pip install django
    
4.  django-admin startproject ChatPrj
    
5.  python manage.py startapp ChatApp
    
6.  Open the project in your code editor.
    
7.  Create a templates folder and register it in the project's settings.
    
8.  Register the app in the project's settings.
    
9.  Create URLs for the app and register them in the project's URLs.
    

### 2\. Installing Libraries

1.  pip install django-channels
    
2.  pip install daphne
    
3.  INSTALLED\_APPS = \[ 'daphne', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'ChatApp', 'channels',\]
    

### 3\. Create Important Files in the App Folder

1.  Create routing.py.
    
2.  Create consumers.py.
    

### 4\. Creating Models

1.  class Room(models.Model): room\_name = models.CharField(max\_length=255) def \_\_str(self): return self.room\_name
    
2.  class Message(models.Model): room = models.ForeignKey(Room, on\_delete=models.CASCADE) sender = models.CharField(max\_length=255) message = models.TextField() def \_\_str(self): return str(self.room)
    
3.  python manage.py makemigrationspython manage.py migrate
    
4.  from .models import \*admin.site.register(Room)admin.site.register(Message)
    

5\. Getting Template Files from GitHub
======================================

*   Download the following HTML templates from GitHub:
    
    *   index.html
        
    *   message.html
        

### 6\. Create Views

1.  def CreateRoom(request): return render(request, 'index.html')
    
2.  def MessageView(request, room\_name, username): return render(request, 'message.html')
    

### 7\. Map Views to URLs:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   from . import views  from django.urls import path  urlpatterns = [      path('', views.CreateRoom, name='create-room'),      path('//', views.MessageView, name='room'),  ]   `

### 8\. View CreateRoom view in browser to make sure setup works

### 9\. Allow users to login or create chat rooms in CreateRoom view

In your index.html file, make sure to include a CSRF token in form:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   {% csrf_token %}   `

In your Django CreateRoom view, check for incoming POST requests:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   if request.method == 'POST':   `

Retrieve user-entered data:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   if request.method == 'POST':      username = request.POST['username']      room = request.POST['room']   `

Create try and except blocks to either get the room object or create it if it does not exist:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   try:      get_room = Room.objects.get(room_name=room)  except Room.DoesNotExist:      new_room = Room(room_name=room)      new_room.save()   `

Test the code to see if it works.

Next, redirect users to MessageView:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   try:      get_room = Room.objects.get(room_name=room)      return redirect('room', room_name=room, username=username)  except Room.DoesNotExist:      new_room = Room(room_name=room)      new_room.save()      return redirect('room', room_name=room, username=username)   `

### 10\. Displaying Messages Created in a Room

1.  Getting the room object and returning it as well as room name and username in the context
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   def MessageView(request, room_name, username):      get_room = Room.objects.get(room_name=room_name)      get_messages = Message.objects.filter(room=get_room)      context = {          "messages": get_messages,          "user": username,          "room_name": room_name,      }      return render(request, 'message.html', context)   `

1.  Display Messages from the Query Set in message.html:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML        `{% for i in messages %}          {% if i.sender != user %}                                   {{i.message}}**-{{i.sender}}**          {% else %}                                  {{i.message}}          {% endif %}      {% endfor %}`    

This code is part of your messages.html file and is responsible for rendering the messages in the chat room. Messages are displayed differently based on whether the sender is the current user or another user.

### 11\. Creating Consumers

Head over to your consumers.py file

1.  Importing Modules:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   import json  from channels.generic.websocket import AsyncWebsocketConsumer  from channels.db import database_sync_to_async  from ChatApp.models import *   `

1.  Creating ChatConsumer:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   class ChatConsumer(AsyncWebsocketConsumer):   `

1.  Create connect Method:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   class ChatConsumer(AsyncWebsocketConsumer):      async def connect(self):          self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"          await self.channel_layer.group_add(self.room_name, self.channel_name)          await self.accept()   `

1.  Create disconnect Method:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   class ChatConsumer(AsyncWebsocketConsumer):      async def connect(self):          self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"          await self.channel_layer.group_add(self.room_name, self.channel_name)          await self.accept()      async def disconnect(self, close_code):          await self.channel_layer.group_discard(self.room_name, self.channel_name)   `

In this code section, you're creating a Django Channels consumer called ChatConsumer. It includes the connect method for WebSocket connection setup and the disconnect method for WebSocket disconnection handling. These consumers are essential for real-time communication in your Django application.

### 12\. Creating URL for ChatConsumer

Head to your routing.py File and Add the Following:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   from django.urls import path  from .consumers import ChatConsumer  websocket_urlpatterns = [      path('ws/notification//', ChatConsumer.as_asgi()),  ]   `

### 13\. Register routing url in asgi.py file in project

Head to your asgi.py file in project folder

1.  Importing Modules:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   import os  from django.core.asgi import get_asgi_application  # imports  from channels.routing import ProtocolTypeRouter, URLRouter  from django.core.asgi import get_asgi_application  from ChatApp import routing  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie.settings')  application = get_asgi_application()   `

1.  Rename application to django\_asgi\_app:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   django_asgi_app = get_asgi_application()   `

1.  Add the Following:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   application = ProtocolTypeRouter({      "http": django_asgi_app,      "websocket": URLRouter(          routing.websocket_urlpatterns      )  })   `

1.  The Final Code:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   import os  from django.core.asgi import get_asgi_application  # imports  from channels.routing import ProtocolTypeRouter, URLRouter  from django.core.asgi import get_asgi_application  from ChatApp import routing  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie.settings')  django_asgi_app = get_asgi_application()  application = ProtocolTypeRouter({      "http": django_asgi_app,      "websocket": URLRouter(          routing.websocket_urlpatterns      )  })   `

### 14\. Adding asgi.py Configurations and channel\_layers to Settings

Head to settings.py file

1.  Update ASGI\_APPLICATION in your Settings:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   ASGI_APPLICATION = "ChatProject.asgi.application"   `

1.  Add channel\_layers Configuration:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   CHANNEL_LAYERS = {      "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},  }   `

Here's the provided content in markdown format for your readme.md file:

### 15\. Creating a New WebSocket

1.  Head to message.html File and Create Script Tags:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   </div><div class="slate-code_line"></div><div class="slate-code_line">   `

This step involves adding script tags to your message.html file to embed JavaScript code for handling WebSocket connections.

1.  Create a New WebSocket:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   </div><div class="slate-code_line">    const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";</div><div class="slate-code_line">    const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notification/{{room_name}}/`;</div><div class="slate-code_line">    const socket = new WebSocket(wsEndpoint);</div><div class="slate-code_line">   ``

In this part of the code, you're creating a new WebSocket connection in your message.html file. It determines the WebSocket protocol based on whether the application is served over HTTPS or HTTP and establishes a connection to the WebSocket endpoint for the specific chat room.

### 16\. Creating Event Handlers for WebSocket Connection

Handling WebSocket Connection Events:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   </div><div class="slate-code_line">    // Determine the WebSocket protocol based on the application&#x27;s URL</div><div class="slate-code_line">    const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";</div><div class="slate-code_line">    const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notification/{{room_name}}/`;</div><div class="slate-code_line"></div><div class="slate-code_line">    // Create a new WebSocket connection</div><div class="slate-code_line">    const socket = new WebSocket(wsEndpoint);</div><div class="slate-code_line"></div><div class="slate-code_line">    // Successful connection event</div><div class="slate-code_line">    socket.onopen = (event) => {</div><div class="slate-code_line">        console.log("WebSocket connection opened!");</div><div class="slate-code_line">    };</div><div class="slate-code_line"></div><div class="slate-code_line">    // Socket disconnect event</div><div class="slate-code_line">    socket.onclose = (event) => {</div><div class="slate-code_line">        console.log("WebSocket connection closed!");</div><div class="slate-code_line">    };</div><div class="slate-code_line">   ``

### 17\. Creating an Event Listener for Sending Messages

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   </div><div class="slate-code_line">    // Determine the WebSocket protocol based on the application&#x27;s URL</div><div class="slate-code_line">    const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";</div><div class="slate-code_line">    const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notification/{{room_name}}/`;</div><div class="slate-code_line"></div><div class="slate-code_line">    // Create a new WebSocket connection</div><div class="slate-code_line">    const socket = new WebSocket(wsEndpoint);</div><div class="slate-code_line"></div><div class="slate-code_line">    // Successful connection event</div><div class="slate-code_line">    socket.onopen = (event) => {</div><div class="slate-code_line">        console.log("WebSocket connection opened!");</div><div class="slate-code_line">    };</div><div class="slate-code_line"></div><div class="slate-code_line">    // Socket disconnect event</div><div class="slate-code_line">    socket.onclose = (event) => {</div><div class="slate-code_line">        console.log("WebSocket connection closed!");</div><div class="slate-code_line">    };</div><div class="slate-code_line"></div><div class="slate-code_line">    // Form submit listener</div><div class="slate-code_line">    document.getElementById(&#x27;message-form&#x27;).addEventListener(&#x27;submit&#x27;, function(event){</div><div class="slate-code_line">        event.preventDefault();</div><div class="slate-code_line">        const message = document.getElementById(&#x27;msg&#x27;).value;</div><div class="slate-code_line">        socket.send(</div><div class="slate-code_line">            JSON.stringify({</div><div class="slate-code_line">                &#x27;message&#x27;: message,</div><div class="slate-code_line">                &#x27;room_name&#x27;: &#x27;{{room_name}}&#x27;,</div><div class="slate-code_line">                &#x27;sender&#x27;: &#x27;{{user}}&#x27;,</div><div class="slate-code_line">            })</div><div class="slate-code_line">        );</div><div class="slate-code_line">    });</div><div class="slate-code_line">   ``

### 18\. Creating Methods in Consumers to Receive and Send New Messages

1.  Creating a ChatConsumer with receive Method:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   import json  from channels.generic.websocket import AsyncWebsocketConsumer  from channels.db import database_sync_to_async  from ChatApp.models import *  class ChatConsumer(AsyncWebsocketConsumer):      async def connect(self):          self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"          await self.channel_layer.group_add(self.room_name, self.channel_name)          await self.accept()      async def disconnect(self, close_code):          await self.channel_layer.group_discard(self.room_name, self.channel_name)      async def receive(self, text_data):          text_data_json = json.loads(text_data)          message = text_data_json   `

1.  Adding a send\_message Method:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   import json  from channels.generic.websocket import AsyncWebsocketConsumer  from channels.db import database_sync_to_async  from ChatApp.models import *  class ChatConsumer(AsyncWebsocketConsumer):      async def connect(self):          self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"          await this.channel_layer.group_add(self.room_name, self.channel_name)          await this.accept()      async def disconnect(self, close_code):          await this.channel_layer.group_discard(self.room_name, self.channel_name)      async def receive(self, text_data):          text_data_json = json.loads(text_data)          message = text_data_json      async def send_message(self, event):          data = event['message']          await self.create_message(data=data)          response_data = {              'sender': data['sender'],              'message': data['message']          }          await self.send(text_data=json.dumps({'message': response_data}))   `

1.  Creating the create\_message Method to Create and Save Messages:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   import json  from channels.generic.websocket import AsyncWebsocketConsumer  from channels.db import database_sync_to_async  from ChatApp.models import *  class ChatConsumer(AsyncWebsocketConsumer):      async def connect(self):          self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"          await self.channel_layer.group_add(self.room_name, self.channel_name)          await self.accept()      async def disconnect(self, close_code):          await self.channel_layer.group_discard(self.room_name, self.channel_name)      async def receive(self, text_data):          text_data_json = json.loads(text_data)          message = text_data_json      async def send_message(self, event):          data = event['message']          await self.create_message(data=data)          response_data = {              'sender': data['sender'],              'message': data['message']          }          await self.send(text_data=json.dumps({'message': response_data}))      @database_sync_to_async      def create_message(self, data):          get_room_by_name = Room.objects.get(room_name=data['room_name'])          if not Message.objects.filter(message=data['message']).exists():              new_message = Message(room=get_room_by_name, sender=data['sender'], message=data['message'])              new_message.save()   `

In this code section, you're defining methods in your Django Channels ChatConsumer to receive, send, and create messages. These methods handle WebSocket communication and message storage in your Django application.

#### 19\. Adding a Socket Event Listener for Server Responses:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML``   </div><div class="slate-code_line">    // Determine the WebSocket protocol based on the application&#x27;s URL</div><div class="slate-code_line">    const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";</div><div class="slate-code_line">    const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notification/{{room_name}}/`;</div><div class="slate-code_line"></div><div class="slate-code_line">    // Create a new WebSocket connection</div><div class="slate-code_line">    const socket = new WebSocket(wsEndpoint);</div><div class="slate-code_line"></div><div class="slate-code_line">    // Successful connection event</div><div class="slate-code_line">    socket.onopen = (event) => {</div><div class="slate-code_line">        console.log("WebSocket connection opened!");</div><div class="slate-code_line">    };</div><div class="slate-code_line"></div><div class="slate-code_line">    // Socket disconnect event</div><div class="slate-code_line">    socket.onclose = (event) => {</div><div class="slate-code_line">        console.log("WebSocket connection closed!");</div><div class="slate-code_line">    };</div><div class="slate-code_line"></div><div class="slate-code_line">    // Form submit listener</div><div class="slate-code_line">    document.getElementById(&#x27;message-form&#x27;).addEventListener(&#x27;submit&#x27;, function(event){</div><div class="slate-code_line">        event.preventDefault();</div><div class="slate-code_line">        const message = document.getElementById(&#x27;msg&#x27;).value;</div><div class="slate-code_line">        socket.send(</div><div class="slate-code_line">            JSON.stringify({</div><div class="slate-code_line">                &#x27;message&#x27;: message,</div><div class="slate-code_line">                &#x27;room_name&#x27;: &#x27;{{room_name}}&#x27;,</div><div class="slate-code_line">                &#x27;sender&#x27;: &#x27;{{user}}&#x27;,</div><div class="slate-code_line">            })</div><div class="slate-code_line">        );</div><div class="slate-code_line">    });</div><div class="slate-code_line"></div><div class="slate-code_line">    // Response from consumer on the server</div><div class="slate-code_line">    socket.addEventListener("message", (event) => {</div><div class="slate-code_line">        const messageData = JSON.parse(event.data)[&#x27;message&#x27;];</div><div class="slate-code_line">        console.log(messageData);</div><div class="slate-code_line"></div><div class="slate-code_line">        var sender = messageData[&#x27;sender&#x27;];</div><div class="slate-code_line">        var message = messageData[&#x27;message&#x27;];</div><div class="slate-code_line"></div><div class="slate-code_line">        // Empty the message input field after the message has been sent</div><div class="slate-code_line">        if (sender == &#x27;{{user}}&#x27;){</div><div class="slate-code_line">            document.getElementById(&#x27;msg&#x27;).value = &#x27;&#x27;;</div><div class="slate-code_line">        }</div><div class="slate-code_line"></div><div class="slate-code_line">        // Append the message to the chatbox</div><div class="slate-code_line">        var messageDiv = document.querySelector(&#x27;.message&#x27;);</div><div class="slate-code_line">        if (sender != &#x27;{{user}}&#x27;) { // Assuming you have a variable `currentUser` to hold the current user&#x27;s name</div><div class="slate-code_line">            messageDiv.innerHTML += &#x27;<div class="receive"><p style="color: #000;">&#x27; + message + &#x27;<strong>-&#x27; + sender + &#x27;</strong></p></div>&#x27;;</div><div class="slate-code_line">        } else {</div><div class="slate-code_line">            messageDiv.innerHTML += &#x27;<div class="send"><p style="color: #000;">&#x27; + message + &#x27;</p></div>&#x27;;</div><div class="slate-code_line">        }</div><div class="slate-code_line">        scrollToBottom();</div><div class="slate-code_line">    });</div><div class="slate-code_line">   ``

1.  Adding a Function for Automatic Scrolling to the Bottom:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   </div><div class="slate-code_line">    function scrollToBottom() {</div><div class="slate-code_line">        var chatContainer = document.getElementById("chatContainer");</div><div class="slate-code_line">        chatContainer.scrollTop = chatContainer.scrollHeight;</div><div class="slate-code_line">    }</div><div class="slate-code_line">   `

### 20\. Testing the Code

In this section, you're creating a JavaScript event listener to handle responses from the server through the WebSocket connection. It updates the chat interface with incoming messages and automatically scrolls to the bottom to display the latest messages.
