# telecom

Welcome! This repository contains a series of hands-on Python networking exercises designed to take you from basic sockets to building proxies and understanding data integrity.

## How to Use This Repository

The learning process is structured to help you learn effectively without accidentally spoiling the solutions.

**1. The `main` Branch**

This is the primary branch for working on the exercises. It contains:
- A folder for each practice session.
- `_todo.py` files with the exercise code you need to complete.
- A `README.md` in each folder explaining the objective and how to run the code.

**2. The `solutions` Branch**

This branch contains all the completed `_solution.py` files.
- **IMPORTANT:** Try your very best to solve the exercise yourself before looking at the solution!
- To view the solutions, switch to the `solutions` branch using the branch dropdown on GitHub or with the command:
  ```bash
  git checkout solutions

## Table of Contents

### [Practice 1: Introduction to Python and File I/O](./Practice_1/)
*   **[Task 1: Years](./Practice_1/Task_1/)** - Reading from text files and processing data.
*   **[Task 2: JSON Calculator](./Practice_1/Task_2/)** - Parsing JSON files and performing calculations.

### [Practice 2: Binary Data Handling](./Practice_2/)
*   **[Task 1: Structs](./Practice_2/Task_1/)** - Reading and writing structured binary data.

### [Practice 3: TCP Sockets I](./Practice_3/)
*   **[Task 1: Simple Echo Server](./Practice_3/Task_1/)** - Your first TCP client-server application.
*   **[Task 2: Persistent Data Server](./Practice_3/Task_2/)** - A server that maintains state between messages.
*   **[Task 3: Multi-Client Server](./Practice_3/Task_3/)** - Handling multiple simultaneous TCP clients.
*   **[Tic Tac Toe](./Practice_3/Tic_Tac_Toe/)** - A complete client-server game application.

### [Practice 4: TCP Sockets II](./Practice_4/)
*   **[Task 1: Basic Client/Server](./Practice_4/Task_1/)** - A refresher on TCP communication.
*   **[Task 2: TCP Calculator](./Practice_4/Task_2/)** - Sending structured data for remote calculations.
*   **[Task 3: Chat Application](./Practice_4/Task_3/)** - Building a multi-user chat room with non-blocking input.

### [Practice 5: UDP and Multicast](./Practice_5/)
*   **[Task 1: UDP Basics](./Practice_5/Task_1/)** - A simple "Hello World" client and server using UDP.
*   **[Task 2: UDP Multicast](./Practice_5/Task_2/)** - Sending a single message to multiple subscribers.
*   **[Task 3: UDP Calculator](./Practice_5/Task_3/)** - Implementing the calculator with a connectionless protocol.
*   **[Task 4: UDP File Transfer](./Practice_5/Task_4/)** - Sending a file in chunks over an unreliable protocol.

### [Practice 6: Proxies and Data Integrity](./Practice_6/)
*   **[Task 1: TCP-to-UDP Proxy](./Practice_6/Task_1/)** - Building a protocol-translating proxy.
*   **[Task 2: Service Discovery](./Practice_6/Task_2/)** - Dynamically finding a server's address.
*   **[Task 3: HTTP Proxy](./Practice_6/Task_3/)** - Intercepting and filtering web traffic.
*   **[Task 4: Parity Error Detection](./Practice_6/Task_4/)** - Understanding simple error detection and correction.
*   **[Task 5: CRC Error Detection](./Practice_6/Task_5/)** - Implementing and analyzing the Cyclic Redundancy Check.

### Prerequisites

- Python 3.8+
- A code editor (like VS Code)
- A terminal or command prompt

Happy coding, and may your packets always reach their destination!