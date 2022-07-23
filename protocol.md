# Protocol Information

## Connections and basic handshakes

### Connection

Start with starting a WebSocket connection to `/ws`. All client-server data will be sent through here.

No initilization message is required.

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

## Connecting to rooms

After logging in to an account through your WebSocket connection, you may connect to a room.

Send a JSON message like this to server through the connection to start the handshake:

```json
{
    "type": "roomconnect",
    "id": 1234
}
```

**Note:** `type` will stay as `"roomconnect"` throughout the entire connection.

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

### Sending

Sending a message to the room after connection is simple. Send a JSON message that looks like this:

```json
{
    "type": "roomconnect",
    "content": "your message content"
}
```

### Exiting

Send the following to end the connection:

```json
{
    "type": "roomconnect",
    "end": true
}
```

## Types

### User

```ts
{
    name: string,
    tag: number
}
```

### Server

```ts
{
    id: number,
    code: string,
    name: string,
    users: Array<User>
}
```

## Reference

Once again, every message should contain the `type` key. Responses will follow the format above (with other keys defined by the payload).

### Registration

#### Schema

**Limit:** `1`

**Type Name:** `"register"`

| Key        | Type     | Description                      |
| ---------- | -------- | -------------------------------- |
| `username` | `string` | Username to create account with. |
| `password` | `string` | Password to create account with. |

#### Response

| Key   | Type     | Description               |
| ----- | -------- | ------------------------- |
| `tag` | `number` | Tag assigned to the user. |

#### Errors

_This operation cannot fail._

#### Example

```json
// SENT BY CLIENT
{
    "type": "register",
    "username": "test",
    "password": "test"
}
// SENT BY SERVER
{
    "type": "register",
    "message": null,
    "done": true,
    "success": true
}
```

### Login

#### Schema

**Limit:** `1`

**Type Name:** `"login"`

| Key        | Type     | Description                           |
| ---------- | -------- | ------------------------------------- |
| `username` | `string` | Username to log in with.              |
| `tag`      | `int`    | Discriminator of the target username. |
| `password` | `string` | Password to log in with.              |

#### Response

_No special values returned._

#### Errors

| Message                           | Reason            |
| --------------------------------- | ----------------- |
| `"Invalid username or password."` | Self-explanatory. |
| `"Already logged in."`            | Self-explanatory. |

### Creating Rooms

#### Schema

**Limit:** No limit

**Type Name:** `"createroom"`

**Authentication is required to perform this operation.**

| Key    | Type     | Description                 |
| ------ | -------- | --------------------------- |
| `name` | `string` | What to name the room with. |

#### Response

| Key  | Type     | Description            |
| ---- | -------- | ---------------------- |
| `id` | `number` | ID of the created room |

#### Errors

_This operation cannot fail._

#### Example

```json
// SENT BY CLIENT
{
    "type": "createroom",
    "name": "test",
}
// SENT BY SERVER
{
    "type": "register",
    "message": null,
    "done": true,
    "success": true,
    "id": "roomid",
}
```

### Joining Rooms

#### Schema

**Limit:** No limit

**Type Name:** `"createroom"`

**Authentication is required to perform this operation.**

| Key    | Type     | Description              |
| ------ | -------- | ------------------------ |
| `code` | `string` | Code of the target room. |

#### Response

| Key  | Type     | Description            |
| ---- | -------- | ---------------------- |
| `id` | `number` | ID of the joined room. |

#### Errors

| Message                | Reason            |
| ---------------------- | ----------------- |
| `"Invalid room code."` | Self-explanatory. |

### Listing Rooms

#### Schema

**Limit:** No limit

**Type Name:** `"listrooms"`

**Authentication is required to perform this operation.**

_No other keys needed._

#### Response

| Key       | Type            | Description                           |
| --------- | --------------- | ------------------------------------- |
| `servers` | `Array<Server>` | Array of servers the user has joined. |

#### Errors

_This operation cannot fail._
