# Distributed Communication Network Simulator

**Course:** CS3551 – Distributed Computing  
**Project topic:** 3. Design and implement a distributed communication network model that demonstrates communication primitives and different message-passing scenarios.

## 1. Problem definition
Distributed applications consist of multiple independent processes that exchange information through messages. This project simulates a small network of four processes and demonstrates common communication primitives without requiring multiple physical computers.

## 2. Objectives
- Model four independent processes: P1, P2, P3 and P4.
- Demonstrate point-to-point (unicast) message passing.
- Demonstrate broadcast and multicast communication.
- Demonstrate request-response communication.
- Maintain an inbox for each process and an event log of message transfers.

## 3. Technologies
- Python 3
- Object-oriented programming
- Queue (`collections.deque`) for message buffering
- No external libraries required

## 4. System architecture

```text
                 +----------------------+
                 |  Distributed Network |
                 |   Message Router     |
                 +----------+-----------+
                            |
             +--------------+--------------+
             |              |              |
          +--v--+        +--v--+        +--v--+       +------+
          | P1  |        | P2  |        | P3  |       | P4   |
          |Inbox|        |Inbox|        |Inbox|       |Inbox |
          +-----+        +-----+        +-----+       +------+
             Each process has an independent message queue
```

## 5. Communication primitives
1. **Unicast:** one sender sends a message to one receiver.
2. **Broadcast:** one sender sends the same message to every other process.
3. **Multicast:** one sender sends a message to a selected group.
4. **Request-response:** a process sends a request and the receiving process returns an acknowledgement.
5. **Asynchronous inbox:** messages are placed in a receiver's queue. The receiver can read them later.

## 6. Algorithm
1. Start the application.
2. Create four processes P1, P2, P3 and P4.
3. Display the communication menu.
4. Accept the user's communication choice.
5. Identify the sender and receiver process IDs.
6. Create a message with a unique message ID.
7. Route the message to the receiver's inbox.
8. For broadcast, repeat delivery for all other processes.
9. For multicast, repeat delivery only for selected processes.
10. For request-response, deliver the request and create an acknowledgement.
11. Display inbox contents or the communication event log.
12. Stop when the user selects Exit.

## 7. How to execute
1. Install Python 3 on the computer.
2. Extract the ZIP file.
3. Open a terminal in the extracted project folder.
4. Run:

```bash
python main.py
```

No `pip install` command is required.

## 8. Sample test cases

| Test | Operation | Expected result |
|---|---|---|
| 1 | P1 sends "Hello" to P2 | Message appears in P2 inbox |
| 2 | P1 broadcasts "Meeting" | P2, P3 and P4 receive it |
| 3 | P1 multicasts to P2 and P3 | Only P2 and P3 receive it |
| 4 | P2 requests data from P3 | P3 receives request and sends ACK |
| 5 | P4 views inbox | All pending messages for P4 are displayed |

## 9. Expected output
The application displays a menu, reports successful message transfers, stores messages in process inboxes, and records each transfer in the communication event log. Message IDs make individual transfers easy to identify.

## 10. Applications
- Distributed chat systems
- Client-server applications
- Group notification systems
- Distributed service requests
- Understanding message-based communication

## 11. Limitations and future enhancement
This is a simulation: all processes run inside one Python program and messages are delivered immediately to in-memory queues. It does not use real network sockets or handle machine failures. It can be extended using TCP sockets, multiple computers, configurable network delay, packet loss, and process-failure detection.

## 12. Conclusion
The Distributed Communication Network Simulator demonstrates how independent processes communicate using unicast, broadcast, multicast, and request-response primitives. Separate inboxes and a communication event log make message flow easy to observe and understand.
