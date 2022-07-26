# Protocol Information

## Connections and basic handshakes

### Connection

Start with starting a WebSocket connection to `/ws`. All client-server data will be sent through here.

No initialization message is required.

### Handshakes

A handshake is considered as a singular or multi message exchange between the server and client. To start a handshake, you should send a message looking something like this:

```json
{
    "type": "type-header-name"
    // rest of payload here
}
```

The `type` key will be present on any server response and should be on every JSON object sent by the client.

#### Responses

A basic response looks like this:

```json
{
    "type": "type-header-passed-in-request",
    "message": "message content",
    "done": true,
    "success": true
}
```

**What's going on here?**

-   `type` mimicks the `type` key sent by the client.
-   `message` gives some information on what happened (note that this may sometimes be `null`)
-   `done` tells the client whether the current handshake has finished or if it expects another message.
-   `success` just says if the operation was successful

The client is free to continue using the socket if it encounters an error, but it may not continue the current handshake.

_More will be added here as protocol is implemented_

## Authentication

### Registration

Use the following table for reference on what JSON to send:

| Key        | Description                                                |
| ---------- | ---------------------------------------------------------- |
| `type`     | Should be `register`                                       |
| `username` | Self-explanatory.                                          |
| `password` | The password in plaintext (this may be subject to change). |

#### Response

Assuming nothing failed, a registration response will look like this something like this:

```json
{
    "type": "register",
    "message": null,
    "done": true,
    "tag": 1, // this number will vary!
    "success": true
}
```

Since usernames are **not** unique, a tag/discriminator is given to a user upon registration.

**The tag is required to log in to an account later.**

### Logging in

Almost exactly the same as registration:

| Key        | Description                   |
| ---------- | ----------------------------- |
| `type`     | Should be `"login"`           |
| `username` | Self-explanatory.             |
| `password` | Self-explanatory.             |
| `tag`      | The tag returned by register. |

There is no special response data.

## Creating, joining, and listing rooms

### Creating

A room can be created by sending the `createroom` type and a name for the room:

```json
{
    "type": "createroom",
    "name": "name of the room here"
}
```

The server will respond with the following:

```json
{
    "id": 1 // id of the room created
    // ...other server response info
}
```

### Joining

**Note:** Joining **is not** the same as connecting. See the "Connecting to rooms" section below for that.

Join a room by sending the code under the `joinroom` type:

```json
{
    "type": "joinroom",
    "code": "8 character room code here"
}
```

The server will respond with the room under the `room` key.

#### Difference between joining and connecting?

-   A join adds the user to the servers member list, whereas connecting allows the client to receive and send messages to the room.
-   Joining can be done via the rooms code, whereas a connection happens via the rooms ID.
-   Joining can happen once, but a connection can happen an infinite amount of times.

### Listing

Listing is the simplest of the three. Just send `listrooms` as the type, and the server will respond with an array of `Room` objects under the `servers` key.

A room object looks like this:

| Key     | Type          | Description                                                |
| ------- | ------------- | ---------------------------------------------------------- |
| `id`    | `number`      | ID number of the room.                                     |
| `code`  | `string`      | The room code used to join.                                |
| `name`  | `string`      | The name of the room.                                      |
| `users` | `Array<User>` | Array of members (user objects) that have joined the room. |

A user object looks like this:

| Key    | Type     | Description                |
| ------ | -------- | -------------------------- |
| `id`   | `number` | ID of the user.            |
| `name` | `string` | Display name of the user.  |
| `tag`  | `number` | Discriminator of the user. |

## Connecting to rooms

After logging in to an account through your WebSocket connection, you may connect to a room.

Send a JSON message like this to server through the connection to start the handshake:

```json
{
    "type": "roomconnect",
    "id": 1234
}
```

**Note:** `type` will stay as `roomconnect` throughout the entire handshake.

If the room doesn't exist or the user has not joined the target room, the server will return an error and end the handshake.

If all goes well, the server will respond with this:

```json
{
    "type": "roomconnect",
    "done": false,
    "message": "Connection established.",
    "success": true
}
```

### Receiving

Now, at any point during this connection you may receive a message from the server that looks like this:

```json
{
    "type": "roomconnect",
    "done": false,
    "message": "New message received.",
    "new": {
        "author": {
            // User object here...
        },
        "content": "new message content here"
    }
}
```

This is the server telling you that a new message was received. It doesn't expect any reply from the client.

You may also receive a message that looks like the following:

```json
{
    "type": "roomconnect",
    "done": false,
    "message": "Message was updated.",
    "update": {
        "id": 0, // id of the updated message
        "content": "new content of the message"
    }
}
```

This also does not expect any reply.

### Sending

Sending a message to the room after connection is simple. Send a JSON message that looks like this:

```json
{
    "type": "roomconnect",
    "content": "your message content",
    "action": "send"
}
```

The `action` key should be present when sending something to the server during the `roomconnect` handshake.

### Getting messages

You can get messages by sending the following:

```json
{
    "type": "roomconnect",
    "actions": "getmessages",
    "skip": 0,
    "take": 10
}
```

This will get the first 10 messages in the room.

-   `skip` is the number of messages to skip
-   `take` is the number of messages to take from the database

The server should respond with an array of `Message` objects under the `messages` key.

A `Message` object looks like this:

| Key          | Type     | Description                   |
| ------------ | -------- | ----------------------------- |
| `id`         | `number` | ID of the message.            |
| `content`    | `string` | Content of the message.       |
| `author`     | `User`   | Author of the message.        |
| `created_at` | `number` | Creation date of the message. |

### Exiting

Send the following to end the connection:

```json
{
    "type": "roomconnect",
    "end": true
}
```

**Note:** Sending `"end": true` will actually close any handshake, not just room connections.

## Reference

### Operations

#### `register`

Register a new account.

_Request_

| Key        | Type     | Description                      |
| ---------- | -------- | -------------------------------- |
| `username` | `string` | Username to create account with. |
| `password` | `string` | Password to create account with. |

_Response_

| Key   | Type     | Description               |
| ----- | -------- | ------------------------- |
| `tag` | `number` | Tag assigned to the user. |

#### `login`

Log in to an account.

_Request_

| Key        | Type     | Description                                 |
| ---------- | -------- | ------------------------------------------- |
| `username` | `string` | Username to login with.                     |
| `tag`      | `number` | Tag assigned to the user upon registration. |
| `password` | `string` | Password to login with.                     |

#### `logout`

Log out of an account.

_No data_

#### `createroom`

Create a new room.

_Request_

| Key    | Type     | Description       |
| ------ | -------- | ----------------- |
| `name` | `string` | Name of the room. |

_Response_

| Key    | Type     | Description                   |
| ------ | -------- | ----------------------------- |
| `id`   | `number` | ID of the newly created room. |
| `code` | `string` | Unique room code to join.     |

#### `joinroom`

Join a room.

_Request_

| Key    | Type     | Description             |
| ------ | -------- | ----------------------- |
| `code` | `string` | Room code to join with. |

_Response_

| Key    | Type   | Description                      |
| ------ | ------ | -------------------------------- |
| `room` | `Room` | Room object for the joined room. |

#### `listrooms`

List all rooms the current user has joined.

_Response_

| Key       | Type          | Description                 |
| --------- | ------------- | --------------------------- |
| `servers` | `Array<Room>` | Array of the users servers. |

#### `leaveroom`

Leave a room.

_Request_

| Key  | Type     | Description    |
| ---- | -------- | -------------- |
| `id` | `number` | Room to leave. |

#### `roomconnect`

Start a indefinite client-server exchange for handling room data.

_Request_

| Key  | Type     | Description         |
| ---- | -------- | ------------------- |
| `id` | `number` | Room to connect to. |

_Response_

**Continous handshake**

### Types

#### `User`

| Key    | Type     | Description               |
| ------ | -------- | ------------------------- |
| `name` | `string` | Display name of the user. |
| `tag`  | `number` | Tag of the user.          |
| `id`   | `number` | ID of the user.           |

#### `Room`

| Key     | Type          | Description                      |
| ------- | ------------- | -------------------------------- |
| `id`    | `number`      | ID of the room.                  |
| `name`  | `string`      | Name of the room.                |
| `code`  | `string`      | Unique room code.                |
| `users` | `Array<User>` | Users that have joined the room. |
