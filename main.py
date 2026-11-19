"""
Distributed Communication Network Simulator
Project 3 - CS3551 Distributed Computing

A console-based simulator for distributed communication primitives:
1. Point-to-point send/receive
2. Broadcast
3. Multicast
4. Request-response
5. Asynchronous message queues

No external packages are required.
"""

from dataclasses import dataclass
from collections import deque
from typing import Dict, List, Optional
import time


@dataclass
class Message:
    message_id: int
    sender: str
    receiver: str
    content: str
    message_type: str
    timestamp: float


class Process:
    def __init__(self, process_id: str):
        self.process_id = process_id
        self.inbox = deque()

    def receive(self) -> Optional[Message]:
        if self.inbox:
            return self.inbox.popleft()
        return None


class DistributedNetwork:
    def __init__(self, process_ids: List[str]):
        self.processes: Dict[str, Process] = {
            pid: Process(pid) for pid in process_ids
        }
        self.message_counter = 0
        self.event_log = []

    def _create_message(self, sender, receiver, content, message_type):
        self.message_counter += 1
        return Message(
            self.message_counter, sender, receiver, content,
            message_type, time.time()
        )

    def _deliver(self, message: Message):
        self.processes[message.receiver].inbox.append(message)
        self.event_log.append(
            f"Message M{message.message_id}: {message.sender} -> "
            f"{message.receiver} | {message.message_type} | {message.content}"
        )

    def send(self, sender: str, receiver: str, content: str):
        """Point-to-point communication."""
        if sender not in self.processes or receiver not in self.processes:
            raise ValueError("Unknown process ID.")
        msg = self._create_message(sender, receiver, content, "UNICAST")
        self._deliver(msg)
        print(f"SUCCESS: {sender} sent a message to {receiver}.")

    def broadcast(self, sender: str, content: str):
        """Send the same message to every other process."""
        if sender not in self.processes:
            raise ValueError("Unknown sender process.")
        for receiver in self.processes:
            if receiver != sender:
                msg = self._create_message(sender, receiver, content, "BROADCAST")
                self._deliver(msg)
        print(f"SUCCESS: {sender} broadcast a message to all other processes.")

    def multicast(self, sender: str, receivers: List[str], content: str):
        """Send a message to a selected group of processes."""
        if sender not in self.processes:
            raise ValueError("Unknown sender process.")
        for receiver in receivers:
            if receiver not in self.processes:
                raise ValueError(f"Unknown receiver: {receiver}")
            if receiver == sender:
                continue
            msg = self._create_message(sender, receiver, content, "MULTICAST")
            self._deliver(msg)
        print(f"SUCCESS: {sender} multicast a message to {receivers}.")

    def request_response(self, sender: str, receiver: str, request: str):
        """Simulate a request followed by a response."""
        self.send(sender, receiver, request)
        received = self.processes[receiver].receive()
        if received is None:
            print("No request available.")
            return
        print(f"{receiver} received request: {received.content}")
        response_text = f"ACK: {received.content}"
        response = self._create_message(receiver, sender, response_text, "RESPONSE")
        self._deliver(response)
        print(f"{receiver} sent a response to {sender}.")

    def show_inbox(self, process_id: str):
        if process_id not in self.processes:
            raise ValueError("Unknown process ID.")
        inbox = self.processes[process_id].inbox
        print(f"\n--- Inbox of {process_id} ---")
        if not inbox:
            print("Inbox is empty.")
        else:
            for msg in inbox:
                print(
                    f"M{msg.message_id} | From: {msg.sender} | "
                    f"Type: {msg.message_type} | Message: {msg.content}"
                )

    def receive_next(self, process_id: str):
        if process_id not in self.processes:
            raise ValueError("Unknown process ID.")
        msg = self.processes[process_id].receive()
        if msg:
            print(
                f"{process_id} received M{msg.message_id} from "
                f"{msg.sender}: {msg.content}"
            )
        else:
            print(f"No messages waiting for {process_id}.")

    def show_log(self):
        print("\n--- Communication Event Log ---")
        if not self.event_log:
            print("No communication events yet.")
        else:
            for event in self.event_log:
                print(event)


def choose_process(network, prompt):
    pid = input(prompt).strip().upper()
    if pid not in network.processes:
        print("Invalid process ID. Available:", ", ".join(network.processes))
        return None
    return pid


def main():
    process_ids = ["P1", "P2", "P3", "P4"]
    network = DistributedNetwork(process_ids)

    print("=" * 58)
    print(" DISTRIBUTED COMMUNICATION NETWORK SIMULATOR")
    print(" CS3551 - Distributed Computing | Project 3")
    print("=" * 58)
    print("Available distributed processes:", ", ".join(process_ids))

    while True:
        print("""
MENU
1. Point-to-point message (Unicast)
2. Broadcast message
3. Multicast message
4. Request-response communication
5. View process inbox
6. Receive next message
7. View communication event log
8. Exit
""")
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                sender = choose_process(network, "Sender (P1-P4): ")
                receiver = choose_process(network, "Receiver (P1-P4): ")
                if sender and receiver:
                    content = input("Enter message: ")
                    network.send(sender, receiver, content)

            elif choice == "2":
                sender = choose_process(network, "Sender (P1-P4): ")
                if sender:
                    content = input("Enter broadcast message: ")
                    network.broadcast(sender, content)

            elif choice == "3":
                sender = choose_process(network, "Sender (P1-P4): ")
                if sender:
                    raw = input("Enter receiver IDs separated by commas (e.g. P2,P3): ")
                    receivers = [x.strip().upper() for x in raw.split(",") if x.strip()]
                    content = input("Enter multicast message: ")
                    network.multicast(sender, receivers, content)

            elif choice == "4":
                sender = choose_process(network, "Requester (P1-P4): ")
                receiver = choose_process(network, "Service process (P1-P4): ")
                if sender and receiver:
                    request = input("Enter request: ")
                    network.request_response(sender, receiver, request)

            elif choice == "5":
                pid = choose_process(network, "Process whose inbox to view: ")
                if pid:
                    network.show_inbox(pid)

            elif choice == "6":
                pid = choose_process(network, "Process that will receive: ")
                if pid:
                    network.receive_next(pid)

            elif choice == "7":
                network.show_log()

            elif choice == "8":
                print("Simulator closed.")
                break

            else:
                print("Invalid choice. Select 1 to 8.")

        except ValueError as error:
            print("ERROR:", error)


if __name__ == "__main__":
    main()
