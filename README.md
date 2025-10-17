# telecom

Welcome! This repository contains a series of hands-on Python networking exercises designed to take you from basic sockets to building proxies and understanding data integrity.

## How to Use This Repository

The learning process is structured to help you learn effectively without accidentally spoiling the solutions.

**1. The `main` Branch (In Progress 🚧)**
This is the primary branch for working on the exercises. It contains:
- A folder for each practice session.
- `_todo.py` files with the exercise code you need to complete.
- A `README.md` in each folder explaining the objective and how to run the code.

**2. The `solutions` Branch (In Progress 🚧)**
This branch contains all the completed `_solution.py` files.
- **IMPORTANT:** Try your very best to solve the exercise yourself before looking at the solution!
- To view the solutions, switch to the `solutions` branch using the branch dropdown on GitHub or with the command:
  ```bash
  git checkout solutions


Of course! This is a fantastic idea. A well-structured GitHub repository is an invaluable tool for students. Here are my suggestions for a funny name, a good description, and a complete guide on how to structure the repo to maximize its educational value.

---

### **1. Name and Description**

A good name is memorable and sets a fun tone. A good description tells students exactly what they're getting into.

#### **Suggested Names (Pick your favorite):**

*   **Socket To 'Em:** A classic, punchy pun.
*   **PyNet Puzzles:** Emphasizes the problem-solving nature of the exercises.
*   **Unreliable Fun Datagrams:** A nerdy inside joke for those who understand UDP.
*   **The Packet Sniffer's Guide:** Sounds adventurous and hands-on.
*   **SYN-ACK-tical Solutions:** Another great networking pun.

#### **Repo Description:**

> A collection of hands-on Python networking exercises designed to take you from basic sockets to building proxies and understanding data integrity. Each exercise provides a `_todo.py` file to complete and a `_solution.py` to check your work. Let's get these packets moving!

---

### **2. How to Make the Repo Most Beneficial (The Complete Guide)**

This is the most important part. A great structure prevents confusion and guides learning.

#### **Step 1: Use a Two-Branch System (Crucial!)**

This is the best way to separate exercises from solutions and prevent students from accidentally seeing the answers.

*   **`main` Branch:** This is the default branch for students. It should contain **only the `_todo.py` files**, the READMEs, and any helper files (like `image_to_send.png`). **DO NOT** put solution files here.
*   **`solutions` Branch:** This branch contains everything from `main`, **plus** all the `_solution.py` files.

**How to set this up:**
1.  Create your repository and do all your initial work on the `main` branch.
2.  Once you have the `_todo` files and READMEs ready, create a new branch from `main` called `solutions`: `git branch solutions`.
3.  Switch to the new branch: `git checkout solutions`.
4.  Add all the `_solution.py` files, commit them, and push the branch: `git push -u origin solutions`.
5.  Switch back to `main` (`git checkout main`) for any future edits to the exercises.

#### **Step 2: Create a Clear Folder Structure**

Don't dump all the files in the root directory. Organize them by practice session or topic.

```
.
├── Practice_01_UDP_Basics/
│   ├── hello_udp_client_todo.py
│   └── hello_udp_server_todo.py
│   └── README.md              <-- Exercise description here!
│
├── Practice_02_File_Transfer/
│   ├── udp_file_client_todo.py
│   ├── udp_file_server_todo.py
│   ├── image_to_send.png
│   └── README.md
│
├── Practice_03_Proxy_and_Select/
│   ├── client.py
│   ├── server.py
│   ├── tcp_udp_proxy_todo.py
│   └── README.md
│
├── Practice_04_Service_Discovery/
│   ├── ..._todo.py files
│   └── README.md
│
├── Practice_05_HTTP_Proxy/
│   ├── netProxy_todo.py
│   └── README.md
│
├── Practice_06_Error_Detection/
│   ├── parity_exercise_todo.py
│   ├── crc_demonstration.py
│   └── README.md
│
├── .gitignore
├── CHEATSHEET.md
└── README.md  <-- Main repo README
```

#### **Step 3: Write a High-Quality Main `README.md`**

This is the front door to your repository. It should be welcoming and informative.

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