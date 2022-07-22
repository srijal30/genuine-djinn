# Protocol Information

## Connections and basic handshakes

### Connection

Start with starting a WebSocket connection to `/ws`. All client-server data will be sent through here.

No initilization message is required.

### Handshakes

A handshake is considered as a singular or multi message exchange between the server and client. After connecting, you should send a message looking something like this:

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
-   `message` gives some information on what happened
-   `done` tells the client whether the current handshake has finished or if it expects another message.
-   `success` just says if the operation was successful

The client is free to continue using the socket if it encounters an error, but it may not continue the current handshake.

_More will be added here as protocol is implemented_
