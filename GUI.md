# GUI Integration Information

Should be all the info you need below. Typed it out real quick so if there is any confusion or typos let me know.

### Debug Menu

A debug menu exists in the menu bar that allows you to change frames for testing purposes. This should be really useful for debugging.

## Functions and Classes

### Switching/Creating Frames

Switching frames can be done by calling the `switch_frame()` method in the main chat window `ChatApp`.

frame: the frame class you would like to switch to
use_old (default False): switch back to old buffer frame instead of creating a fresh frame

### Frames (frames.py)

Frame classes contain `self.master` which is passed down from the main window `ChatApp`. So for example, to switch frames inside a frame class you can do `self.master.switch_frame()`.

### Menus (menus.py)

Custom menu classes are created using the submenu classes. Menu setting is done for the entire window inside `ChatApp`.

### Submenus (submenus.py)

`parent` - the parent menu class
`master` - the master window `ChatApp`

Don't worry about this for now. Needs some more cleanup before it can be integrated.

## Where to hook into for integration

### Registration

`LoginFrame` > `on_register()`

`LoginFrame` has a basic registration form. On a button press or Return/Enter press (inside an entry box), the `on_register()` method is called. Inside this method is where the registration request can be sent.

### Login

`LoginFrame` > `on_login()`

`LoginFrame` has a basic login form. On a button press or Return/Enter press (inside an entry box), the `on_login()` method is called. Inside this method is where the login request can be sent.

### Create Room

`ConnectFrame` > `on_create()`

`ConnectFrame` has a basic creating room form. On a button press or Return/Enter press (inside an entry box), the `on_create()` method is called. Inside this method is where the room creation request can be sent.

### Join Room

`ConnectFrame` > `on_join()`

`ConnectFrame` has a basic join room form. On a button press or Return/Enter press (inside an entry box), the `on_join()` method is called. Inside this method is where the room joining request can be sent.

### Leaving Room

`ChatFrame` > `on_leave()`

`ChatFrame` has a Leave button. Pressing the button calls the `on_leave()` method. Inside this method is where the leaving room request can be sent.

### Sending Message

`ChatApp` > `send_message()`

When the user sends a message in the GUI, the `on_send()` method inside the `ChatFrame` class for the given room is called. This method sanitizes the text and then calls the `send_message()` method inside the main chat window class `ChatApp`. Should be able to hook directly into `send_message()`. 

### Receiving Message

`ChatApp` > `receive_message()`

Receiving a message is done by sending the message to the `receive_message()` method inside the main window class `ChatApp` (app.py). This can be called by using the `application` variable in `main.py` to get the `ChatApp` class like `application.receive_message(message)`. Inside `receive_message()` is a call to `display_message()` that is a method of `ChatFrame` to display the message string.